import tkinter as tk
from typing import Union

from app.helpers.constants import colors
from app.objects import AbstractImageObject, Position


class AbstractCraftsman(AbstractImageObject):
    craftsman_id: str
    is_played: bool
    is_chosen: bool
    border: Union[None, int]
    wrapper: Union[None, int]

    def __init__(self, position: Position, craftsman_id: str, image_path: str):
        super().__init__(position=position, image_path=image_path)
        self.craftsman_id = craftsman_id
        self.is_played = False
        self.is_chosen = False
        self.border = None
        self.wrapper = None

    def delete(self, canvas: tk.Canvas):
        super().delete(canvas=canvas)
        if self.border:
            canvas.delete(self.border)
            self.border = None
        if self.wrapper:
            canvas.delete(self.wrapper)
            self.wrapper = None
        self.is_chosen = False

    def remove_wrapper(self, canvas: tk.Canvas):
        if self.wrapper:
            canvas.delete(self.wrapper)
            self.wrapper = None
        self.is_chosen = False

    def remove_border(self, canvas: tk.Canvas):
        if self.border:
            canvas.delete(self.border)
            self.border = None
        self.is_chosen = False

    def display_border(self, rect_width: int, rect_height: int, canvas: tk.Canvas):
        x1 = self.position.x * rect_width
        y1 = self.position.y * rect_height
        x2 = x1 + rect_width
        y2 = y1 + rect_height

        self.is_chosen = True
        if not self.border:
            self.border = canvas.create_rectangle(x1, y1, x2, y2, width=5, outline=colors.BORDER_COLOR)
