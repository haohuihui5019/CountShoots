import torch.jit
from Networks import ALTGVT
import numpy as np
import torchvision.transforms as transforms
from PIL import Image
import torch
import torch.nn.functional as F
import cv2
import os

model_path = 'model_best/best_model_mae-7.94_epoch-962.pth'
model = ALTGVT.alt_gvt_large(pretrained=False)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()


def vis(impath):
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # set vis gpu
    device = torch.device('cuda')
    crop_size = 256
    image_path = impath  # 绝对路径
    if not os.path.exists(image_path):
        print("not find image path!")
        exit(-1)

    print("detect image '%s'..." % image_path)
    if not os.path.exists(image_path):
        print("not find image path!")
        exit(-1)
    image = Image.open(image_path).convert("RGB")
    wd, ht = image.size
    st_size = 1.0 * min(wd, ht)
    if st_size < crop_size:
        rr = 1.0 * crop_size / st_size
        wd = round(wd * rr)
        ht = round(ht * rr)
        st_size = 1.0 * min(wd, ht)
        image = image.resize((wd, ht), Image.BICUBIC)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = transform(image)
    with torch.no_grad():

        inputs = image.unsqueeze(0)
        crop_imgs, crop_masks = [], []
        b, c, h, w = inputs.size()
        rh, rw = 256, 256
        for i in range(0, h, rh):
            gis, gie = max(min(h - rh, i), 0), min(h, i + rh)
            for j in range(0, w, rw):
                gjs, gje = max(min(w - rw, j), 0), min(w, j + rw)
                crop_imgs.append(inputs[:, :, gis:gie, gjs:gje])
                mask = torch.zeros([b, 1, h, w])
                mask[:, :, gis:gie, gjs:gje].fill_(1.0)
                crop_masks.append(mask)
        crop_imgs, crop_masks = map(lambda x: torch.cat(x, dim=0), (crop_imgs, crop_masks))

        crop_preds = []
        nz, bz = crop_imgs.size(0), 1
        for i in range(0, nz, bz):
            gs, gt = i, min(nz, i + bz)
            crop_pred, _ = model(crop_imgs[gs:gt])

            _, _, h1, w1 = crop_pred.size()
            crop_pred = F.interpolate(crop_pred, size=(h1 * 8, w1 * 8), mode='bilinear', align_corners=True) / 64

            crop_preds.append(crop_pred)
        crop_preds = torch.cat(crop_preds, dim=0)

        # splice them to the original size
        idx = 0
        pred_map = torch.zeros([b, 1, h, w])
        for i in range(0, h, rh):
            gis, gie = max(min(h - rh, i), 0), min(h, i + rh)
            for j in range(0, w, rw):
                gjs, gje = max(min(w - rw, j), 0), min(w, j + rw)
                pred_map[:, :, gis:gie, gjs:gje] += crop_preds[idx]
                idx += 1
        # for the overlapping area, compute average value
        mask = crop_masks.sum(dim=0).unsqueeze(0)
        pred_map = pred_map / mask
        pred_map = pred_map.squeeze(0).squeeze(0).cpu().data.numpy()
        path = image_path
        path = path.split(".")[-2]
        save_path = os.path.join("%s" % path)
        # print(save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # self.textEdit1.setText("    finish")
        num = pred_map.sum().astype(int)
        with open("%s/pred_map.txt" % save_path, "w") as f:
            f.write(image_path.split("/")[-1] + " " + str(num))
        # textEdit.setText("predmap count is %d" % (num))
        vis_img = pred_map
        # normalize density map values from 0 to 1, then map it to 0-255.
        vis_img = (vis_img - vis_img.min()) / (vis_img.max() - vis_img.min() + 1e-5)
        vis_img = (vis_img * 255).astype(np.uint8)
        vis_img = cv2.applyColorMap(vis_img, cv2.COLORMAP_JET)
        cv2.imwrite("%s/pred_map.png" % save_path, vis_img)
        print("the visual result saved in %s" % save_path)

    return str(num)
