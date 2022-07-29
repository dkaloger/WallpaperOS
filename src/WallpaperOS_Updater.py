import requests
import os


path = "C:\WallpaperOS"
versionR = requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Version.txt")
def Update():
    
   # path = os.path.expanduser('~') +"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    open(path+"/WallpaperOS.exe", "wb").write(requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/WallpaperOS.exe").content)
    open(path+"/Version.txt", "wb").write(requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Version.txt").content)
  #  open(path+"/uninstaller.exe", "wb").write(requests.get("https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/uninstaller.exe").content)    


if not (os.path.exists(path+"/Version.txt")):
    Update()

elif (versionR.text!= open(path+"/Version.txt").read()):
    Update()


os.system(path+"/WallpaperOS.exe")
