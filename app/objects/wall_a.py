import tkinter as tk

from app.helpers.constants import colors
from app.objects import AbstractColorObject, Position


class WallA(AbstractColorObject):
    def __init__(self, position: Position):
        super().__init__(position=position, color=colors.WALL_A_COLOR)

    def revert_color(self, canvas: tk.Canvas):
        canvas.itemconfig(self.rectangle, fill=colors.WALL_A_COLOR)

    def change_color(self, canvas: tk.Canvas):
        canvas.itemconfig(self.rectangle, fill=colors.CHOOSE_COLOR)
