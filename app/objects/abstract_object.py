import tkinter as tk
from typing import Union

from app.helpers.enums import ActionType
from app.objects import Position


class AbstractObject:
    position: Position
    rectangle: Union[None, int]
    is_close_territory_a: bool
    is_close_territory_b: bool
    is_open_territory_a: bool
    is_open_territory_b: bool

    def __init__(self, position: Position):
        self.position: Position = position
        self.is_close_territory_a = False
        self.is_close_territory_b = False
        self.is_open_territory_a = False
        self.is_open_territory_b = False
        self.rectangle = None

    def delete(self, canvas: tk.Canvas):
        if self.rectangle:
            canvas.delete(self.rectangle)
            self.rectangle = None

    def raise_rectangle(self, canvas: tk.Canvas):
        canvas.tag_raise(self.rectangle)

    def display(self, rect_width: int, rect_height: int, canvas: tk.Canvas):
        pass

    def display_when_having_resize_event(self, rect_width: int, rect_height: int, canvas):
        pass
