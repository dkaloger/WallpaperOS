
from tkinterhtml import HtmlFrame
import tkinter as tk

root = tk.Tk()

frame = HtmlFrame(root, horizontal_scrollbar="auto")
 
frame.set_content("<html></html>")

frame.set_content(urllib.request.urlopen("http://thonny.cs.ut.ee").read().decode())