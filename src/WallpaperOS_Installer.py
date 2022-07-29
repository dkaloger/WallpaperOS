import urllib.request
import os
import sys

if getattr(sys, 'frozen', False):
    Installerpath = os.path.dirname(sys.executable) + "\WallpaperOS_Installer.exe"
elif __file__:
    Installerpath = os.path.dirname(__file__) + "\WallpaperOS_Installer.py"

path = os.path.expanduser('~') +"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
#WallpaperOS_Updater
#AI_Wallpaper.exe
urllib.request.urlretrieve("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/WallpaperOS_Updater.exe", path+"/WallpaperOS_Updater.exe")



os.startfile(path+"/WallpaperOS_Updater.exe")


print("Installation Succesfull. Delete installer? y/n ")



x = input()
if (x=="y"):
    os.remove(Installerpath)

