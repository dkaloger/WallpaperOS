import shutil
import os
print("Are you sure you want to delete WallpaperOS? y/n")
x = input()
if (x=="y"):
    if os.path.exists(os.path.expanduser('~') +"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/WallpaperOS_Updater.exe") :
        os.remove(os.path.expanduser('~') +"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/WallpaperOS_Updater.exe")
    
    if os.path.exists("C:\WallpaperOS") :
        shutil.rmtree("C:\WallpaperOS")

