import tkinter as tk

from PIL import Image, ImageTk

from app.objects import AbstractObject, Position


class AbstractImageObject(AbstractObject):
    image_path: str
    image: Image

    def __init__(self, position: Position, image_path: str):
        super().__init__(position=position)
        self.image_path = image_path
        self.image = None

    def display(self, rect_width: int, rect_height: int, canvas: tk.Canvas):
        x1 = self.position.x * rect_width
        y1 = self.position.y * rect_height
        x2 = x1 + rect_width
        y2 = y1 + rect_height

        image = Image.open(self.image_path)
        resized_image = image.resize((int(x2-x1), int(y2-y1)))
        self.image = ImageTk.PhotoImage(resized_image)

        self.rectangle = canvas.create_image(x1, y1, image=self.image, anchor=tk.NW)

    def display_when_having_resize_event(self, rect_width: int, rect_height: int, canvas: tk.Canvas):
        x1 = self.position.x * rect_width
        y1 = self.position.y * rect_height
        x2 = x1 + rect_width
        y2 = y1 + rect_height

        image = Image.open(self.image_path)
        resized_image = image.resize((int(x2-x1), int(y2-y1)))
        self.image = ImageTk.PhotoImage(resized_image)
        canvas.itemconfig(self.rectangle, image=self.image)
        canvas.coords(self.rectangle, x1, y1)
