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
def add_to_startup():
    
        
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "AI_Wallpaper.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' %str( application_path) + "\AI_Wallpaper.exe")
        #pathlib.Path(__file__).resolve()
now = datetime.now() 
response = requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Images/"+ now.strftime("%m-%d-%Y")+ ".png")
img = Image.open(BytesIO(response.content))
img.save(application_path+"/Wallpaper.jpg");
add_to_startup()
ctypes.windll.user32.SystemParametersInfoW(20, 0, application_path +"/Wallpaper.jpg"  , 0)


