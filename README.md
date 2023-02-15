# CountShoots

Code of the paper CountShoots: Automatic detection and counting of slash pine new shoots using UAV imagery.
***
# Architecture
```
|--CountShoots
    |--logs            # saving running logs here
    |--model_path.txt      # saving the trained model parameter links here
    |--app.py         # run file here
    |--yolo.py        # capturing the picture to a specific target and saving it
    |--predict.py      # predicting image-specific targets
    |--model.py       # conducting specific object count detection
```
# Run
python app.py

# Model
This project has trained two parts in the model download link is as follows: 

Plant extraction model: The best plant extraction model can be downloaded from [here](https://pan.baidu.com/s/1aZN_R5_FNIYxJXmpY9vkxw?pwd=1d3w) with the password 1d3w

Shoots counting model: The best shoot counting model can be downloaded from [here](https://pan.baidu.com/s/1eBBIN5PlB_HAnVkzhiElMA?pwd=dpjj) with password dpjj

# Requirments
```
torch==1.10.0+cu113
torchvision==0.11.1+cu113
numpy>=1.16.5
scipy>=1.3.0
opencv-python
timm==0.4.12
matplotlib==3.1.2
opencv_python==4.1.2.30
torch==1.2.0
tqdm==4.60.0
Pillow==8.2.0
h5py==2.10.0 
wandb 
pillow
gradio
gdown
```
