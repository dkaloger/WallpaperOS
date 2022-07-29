import urllib.request
import requests
import os


path = "C:\WallpaperOS"
versionR = requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Version.txt")
def Update():
    
    urllib.request.urlretrieve("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/WallpaperOS.exe", path+"/WallpaperOS.exe")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Version.txt", path+"/Version.txt")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Uninstaller.exe", path+"/Uninstaller.exe")

if not os.path.exists(path):
    os.makedirs(path)

if not (os.path.exists(path+"/Version.txt")):
    Update()

elif (versionR.text!= open(path+"/Version.txt").read()):
    Update()


os.startfile(path+"/WallpaperOS.exe")
