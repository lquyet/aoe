import tkinter as tk

from app.objects import AbstractObject, Position


class AbstractColorObject(AbstractObject):
    color: str

    def __init__(self, position: Position, color: str):
        super().__init__(position=position)
        self.color = color

    def display(self, rect_width: int, rect_height: int, canvas: tk.Canvas):
        x1 = self.position.x * rect_width
        y1 = self.position.y * rect_height
        x2 = x1 + rect_width
        y2 = y1 + rect_height

        self.rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)

    def display_when_having_resize_event(self, rect_width: int, rect_height: int, canvas: tk.Canvas):
        x1 = self.position.x * rect_width
        y1 = self.position.y * rect_height
        x2 = x1 + rect_width
        y2 = y1 + rect_height

        if not self.rectangle:
            self.rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
        rect_coords = (x1, y1, x2, y2)
        canvas.coords(self.rectangle, rect_coords)
