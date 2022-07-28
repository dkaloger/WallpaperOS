from PIL import Image 
import requests
from io import BytesIO
import ctypes
import pathlib
from datetime import datetime
now = datetime.now() 
response = requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Images/"+ now.strftime("%m-%d-%Y")+ ".png")
img = Image.open(BytesIO(response.content))
img.save("Wallpaper.jpg");
ctypes.windll.user32.SystemParametersInfoW(20, 0, pathlib.Path().resolve().__str__() +"/Wallpaper.jpg"  , 0)


