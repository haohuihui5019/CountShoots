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

Plant extraction models and Shoots counting model are available from the Google Cloud Disk link provided [here](https://drive.google.com/drive/folders/1VPvSQLNZcN59cFrX5FQLsbFe32mmYggw?usp=share_link).

Also available from our OneDrive link. [link](https://zqy7y-my.sharepoint.com/:f:/g/personal/lin_zqy7y_onmicrosoft_com/Eop0v_JudAxBoYrpk2sMNowBpjUBVWD9E2KMLoxOQ_LWYA?e=gxIZ0t)

After downloading, please put the Plant extraction model and Shoots counting model under the model_best folder.

# Requirments
```
python>=3.6.0
pytorch>=1.5.1
pyqt>=5.9.2
flask>=2.0.0
numpy>=1.16.5
scipy>=1.3.0
werkzeug>=2.0.3
jinja2>=3.0.3
torch==1.10.0+cu113
torchvision==0.11.1+cu113
timm==0.4.12
matplotlib==3.1.2
opencv_python==4.1.2.30
tqdm==4.60.0
Pillow==8.2.0
h5py==2.10.0 
wandb 
pillow
gradio
gdown
```
