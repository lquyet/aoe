from app.objects import AbstractImageObject, Position


class Castle(AbstractImageObject):
    def __init__(self, position: Position):
        super().__init__(position=position, image_path="../images/castle.png")
