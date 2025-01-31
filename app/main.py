import os
import tkinter as tk

from app.helpers.constants import INIT_WIDTH, INIT_HEIGHT, INFO_BOARD_WIDTH
from map_controller import MapController


def resize(event):
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    frame.config(width=window_width, height=window_height)
    canvas.config(width=window_width - INFO_BOARD_WIDTH, height=window_height)
    map_controller.resize()


def key_press(event):
    keysym: str = event.keysym
    map_controller.on_key_press(keysym=keysym)


def key_release(event):
    keysym: str = event.keysym
    map_controller.on_key_release(keysym=keysym)


window = tk.Tk()
window.geometry(f"{INIT_WIDTH}x{INIT_HEIGHT}")
window.bind("<Configure>", resize)
window.title("AOE")
icon = tk.PhotoImage(file="images/aoe.png")
window.iconphoto(True, icon)
window.bind("<KeyPress>", key_press)
window.bind("<KeyRelease>", key_release)

frame = tk.Frame(window, width=INIT_WIDTH, height=INIT_HEIGHT)
frame.pack(anchor=tk.NW)

canvas = tk.Canvas(frame, width=INIT_WIDTH-INFO_BOARD_WIDTH, height=INIT_HEIGHT)
canvas.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)

map_controller = MapController(window=window, canvas=canvas, frame=frame)
map_controller.update_timer()

window.mainloop()
os.system('xset r off')
