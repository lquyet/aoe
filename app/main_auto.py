import json
import os
import tkinter as tk

from app.helpers.constants import INIT_WIDTH, INIT_HEIGHT, INFO_BOARD_WIDTH
from app.helpers.enums import Side
from app.players.player_alg_1 import PlayerAlgorithm1


def resize(event):
    map_controller.resize()


def key_press(event):
    for i in range(60):
        map_controller.play()
    map_controller.display_map()

def key_release(event):
    keysym: str = event.keysym
    map_controller.on_key_release(keysym=keysym)


window = tk.Tk()
window.geometry(f"{INIT_WIDTH}x{INIT_HEIGHT}")
window.bind("<Configure>", resize)
window.title("AOE")
icon = tk.PhotoImage(file="../images/aoe.png")
window.iconphoto(True, icon)
window.bind("<KeyPress>", key_press)
# window.bind("<KeyRelease>", key_release)

frame = tk.Frame(window, width=INIT_WIDTH, height=INIT_HEIGHT)
frame.pack(anchor=tk.NW)

canvas = tk.Canvas(frame, width=INIT_WIDTH-INFO_BOARD_WIDTH, height=INIT_HEIGHT)
canvas.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)

raw_data = open("../fake_data.json")
json_data: dict = json.load(raw_data)

map_controller = PlayerAlgorithm1(window=window, canvas=canvas, frame=frame, side=Side.A)
map_controller.init_map(json_data=json_data)
map_controller.display_map()

window.mainloop()
os.system('xset r off')
