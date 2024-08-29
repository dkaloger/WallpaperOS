import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import requests, os, sys, threading, ctypes, hashlib
from io import BytesIO
from datetime import datetime
import math
import pystray
from pystray import MenuItem as item
from PIL import Image as PILImage

popup_window = None
application_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', False):
    # Running in a bundle
    base_path = sys._MEIPASS
else:
    # Running in normal Python environment
    base_path = application_path

def create_startup_bat(exe_path):
    # Define the startup folder path
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    # Name of the .bat file
    bat_file_path = os.path.join(startup_folder, 'autorun_WallpaperOS.bat')
    
    # Check if the .exe exists
    if not os.path.exists(exe_path):
        print(f"Error: The specified .exe file was not found: {exe_path}")
        sys.exit(1)
    
    # Content of the .bat file
    bat_content = f'@echo off\n"{exe_path}"\n'
    
    # Create or update the .bat file in the startup folder
    with open(bat_file_path, 'w') as bat_file:
        bat_file.write(bat_content)
    
    print(f"The .bat file has been created/updated at: {bat_file_path}")
def stable_image_number(days_since_epoch, total_images):
    hash_value = hashlib.sha256(str(days_since_epoch).encode()).hexdigest()
    return (int(hash_value, 16) % total_images) + 1

def create_cache_directory():
    cache_dir = os.path.join(application_path, "cache")
    if not os.path.exists(cache_dir): os.makedirs(cache_dir)
    return cache_dir

def is_image_cached(image_number, file_extension=".jpg"):
    cached_image_path = os.path.join(create_cache_directory(), f"Wallpaper_{image_number}{file_extension}")
    return os.path.exists(cached_image_path), cached_image_path

def save_image_to_cache(image_number, img, file_extension=".jpg"):
    img.save(os.path.join(create_cache_directory(), f"Wallpaper_{image_number}{file_extension}"))

def center_window(window, width, height):
    window.geometry(f'{width}x{height}+{(window.winfo_screenwidth()//2)-(width//2)}+{(window.winfo_screenheight()//2)-(height//2)}')

def position_bottom_right(window, width, height):
    window.geometry(f'{width}x{height}+{window.winfo_screenwidth()-width-20}+{window.winfo_screenheight()-height-85}')

def get_total_images():
    info_url = "https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Images/FLUX/Info.txt"
    response = requests.get(info_url)
    if response.status_code == 200: return int(response.text.strip())
    return None

def fetch_and_display_image(image_number):
    loading_label.pack(side="top", pady=20)
    image_label.pack_forget()
    is_cached, cached_image_path = is_image_cached(image_number)
    if is_cached: img = Image.open(cached_image_path)
    else:
        response = requests.get(f"{base_url}{image_number}.jpg")
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            save_image_to_cache(image_number, img)
        else: return
    img_tk = ImageTk.PhotoImage(img.resize((300, 169)))
    loading_label.pack_forget()
    image_label.config(image=img_tk)
    image_label.image = img_tk
    image_label.pack(side="top", pady=20)
    wallpaper_path = os.path.join(application_path, "Wallpaper.jpg")
    img.save(wallpaper_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 0)

def fetch_image_threaded(image_number):
    threading.Thread(target=fetch_and_display_image, args=(image_number,)).start()

def set_wallpaper_for_day_offset(day_offset):
    days_since_epoch = (datetime.now() - datetime(1970, 1, 1)).days + day_offset
    image_number = stable_image_number(days_since_epoch, total_images)
    fetch_image_threaded(image_number)

def load_image_buttons_async(frame, i):
    is_cached, cached_thumbnail_path = is_image_cached(i + 1, file_extension=".webp")
    if is_cached: img = Image.open(cached_thumbnail_path)
    else:
        img_url = f"{raw_base_url}{i + 1}.webp"
        response = requests.get(img_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            save_image_to_cache(i + 1, img, file_extension=".webp")
        else: return
    img_tk = ImageTk.PhotoImage(img.resize((100, 56)))
    btn = tk.Button(frame, image=img_tk, command=lambda i=i: [fetch_image_threaded(i + 1), frame.master.destroy()])
    btn.image = img_tk
    btn.grid(row=i // 10, column=i % 10, padx=5, pady=5)

def close_popup(event=None):
    if popup_window and popup_window.winfo_exists():
        popup_window.destroy()

def open_image_selection_popup():
    global popup_window
    if popup_window and popup_window.winfo_exists(): 
        popup_window.destroy()
    else:
        popup_window = Toplevel(root)
        popup_window.title("Select Image")
        popup_window.configure(bg='black')
        popup_window.resizable(False, False)
        center_window(popup_window, 1160, 75 * (math.ceil(total_images / 10)))
        frame = tk.Frame(popup_window, bg='black')
        popup_window.iconphoto(False, tk.PhotoImage(file=os.path.join(base_path, "tray_icon.png")))
        frame.pack(fill="both", expand=True)
        for i in range(total_images):
            threading.Thread(target=load_image_buttons_async, args=(frame, i)).start()

        # Bind the minimize event to close the popup window
        popup_window.bind("<Unmap>", close_popup)

def hide_window(): 
    root.withdraw() 
    close_popup()
def show_window(): root.deiconify()

def quit_app(icon, item):
    icon.stop()
    root.quit()

def setup_tray():
    image = PILImage.open(os.path.join(base_path, "tray_icon_light.png"))
    menu = (item('Show UI', lambda: [show_window()]), item('Exit', quit_app))
    icon = pystray.Icon("Wallpaper Selector", image, "Wallpaper Selector", menu)
    icon.run()

def load_lock_state():
    settings_file = os.path.join(application_path, "settings.txt")
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file: return file.read().strip() == "locked"
    return False

def save_lock_state(locked):
    with open(os.path.join(application_path, "settings.txt"), "w") as file: file.write("locked" if locked else "unlocked")

def toggle_lock():
    global lock_state
    lock_state = not lock_state
    lock_button.config(image=lock_icon if lock_state else unlock_icon)
    save_lock_state(lock_state)

def animate_loading(frame_index):
    frame = loading_frames[frame_index]
    loading_label.config(image=frame)
    root.after(100, animate_loading, (frame_index + 1) % len(loading_frames))

base_url = "https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Images/FLUX/Upscaled/upscayl_jpg_realesrgan-x4plus_3840px/"
raw_base_url = "https://raw.githubusercontent.com/dkaloger/AIwallpaperimages/main/Images/FLUX/Raw/"
total_images = get_total_images()
exe_path = os.path.abspath("WallpaperOS.exe")
create_startup_bat(os.path.join(application_path, "WallpaperOS.exe"))

root = tk.Tk()
root.title("Wallpaper Selector")
root.iconphoto(False, tk.PhotoImage(file=os.path.join(base_path, "tray_icon.png")))
root.configure(bg='black')
position_bottom_right(root, 400, 300)
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", hide_window)
root.bind("<Unmap>", lambda event: hide_window() if root.state() == "iconic" else None)
lock_state = load_lock_state()

loading_gif = Image.open(os.path.join(base_path, "Loading.gif"))
loading_frames = []

# Iterate through each frame of the GIF and add it to the list
for frame in range(loading_gif.n_frames):
    loading_gif.seek(frame)
    frame_image = loading_gif.copy().resize((50, 50))  # Resize if necessary
    loading_frames.append(ImageTk.PhotoImage(frame_image))
loading_label = tk.Label(root, bg='black')
animate_loading(0)

image_label = tk.Label(root, bg='black')

lock_icon = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "lock.png")).resize((30, 30)))
unlock_icon = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "unlock.png")).resize((30, 30)))
Select_Image = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "Select_Image.png")).resize((30, 30)))
Back_icon = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "Back.png")).resize((30, 30)))
Yesterday_icon = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "Yesterday.png")).resize((30, 30)))

button_frame = tk.Frame(root, bg='black')
tk.Button(button_frame, image=Yesterday_icon, command=lambda: set_wallpaper_for_day_offset(-1), bg='black', border=0, activebackground="black").pack(side="left", padx=20)
tk.Button(button_frame, image=Select_Image, command=open_image_selection_popup, bg='black', border=0, activebackground="black").pack(side="left", padx=20)
lock_button = tk.Button(button_frame, image=lock_icon if lock_state else unlock_icon, command=toggle_lock, bg='black', border=0, activebackground="black")
lock_button.pack(side="left", padx=20)
tk.Button(button_frame, image=Back_icon, command=lambda: set_wallpaper_for_day_offset(0), bg='black', border=0, activebackground="black").pack(side="left", padx=20)
button_frame.pack(side="bottom", pady=20)

if not lock_state:
    set_wallpaper_for_day_offset(0)
else:
    wallpaper_path = os.path.join(application_path, "Wallpaper.jpg")
    img_tk = ImageTk.PhotoImage(Image.open(wallpaper_path).resize((300, 169)))
    image_label.config(image=img_tk)
    image_label.image = img_tk
    image_label.pack(side="top", pady=20)

hide_window()
threading.Thread(target=setup_tray, daemon=True).start()
root.mainloop()
