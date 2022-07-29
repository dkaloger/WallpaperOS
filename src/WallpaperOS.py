from PIL import Image 
import requests
from io import BytesIO
import ctypes
import pathlib
from datetime import datetime

import getpass
import os,sys
USER_NAME = getpass.getuser()

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

now = datetime.now() 
response = requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Images/"+ now.strftime("%m-%d-%Y")+ ".png")
img = Image.open(BytesIO(response.content))
img.save(application_path+"/Wallpaper.jpg");
ctypes.windll.user32.SystemParametersInfoW(20, 0, application_path +"/Wallpaper.jpg"  , 0)
