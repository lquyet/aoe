from app.helpers.constants import colors
from app.objects import AbstractColorObject, Position


class Pond(AbstractColorObject):
    def __init__(self, position: Position):
        super().__init__(position=position, color=colors.POND_COLOR)