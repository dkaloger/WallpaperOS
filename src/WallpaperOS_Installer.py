import requests
import os
path = "C:\WallpaperOS"

bat_path = os.path.expanduser('~') +"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup" 
with open(bat_path + '\\' + "WallpaperOS.bat", "w+") as bat_file:
    bat_file.write("start C:\WallpaperOS\WallpaperOS_Updater.exe")

if not os.path.exists(path):
    os.makedirs(path)

open(path+"/WallpaperOS_Updater.exe", "wb").write(requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/WallpaperOS_Updater.exe").content)
os.system(path+"/WallpaperOS_Updater.exe")

print("Installation Succesfull. Press any key to close...")
x = input()





