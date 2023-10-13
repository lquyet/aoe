import tkinter as tk

from app.helpers.constants import INIT_WIDTH, INIT_HEIGHT, INFO_BOARD_WIDTH
from app.players.player_alg_1 import PlayerAlgorithm1


def resize(event):
    player_1.resize()


def key_press(event):
    for i in range(1):
        player_1.refresh()
        player_2.refresh()
        player_1.refresh()
    player_1.display_map()


def key_release(event):
    keysym: str = event.keysym


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

player_1 = PlayerAlgorithm1(window=window, canvas=canvas, frame=frame, team_id=0)
player_2 = PlayerAlgorithm1(window=None, canvas=None, frame=None, team_id=1)
player_1.create_map()
player_2.create_map()
player_1.display_map()


window.mainloop()
