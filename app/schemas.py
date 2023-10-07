from app.helpers.enums import ActionType
from app.objects import Position, AbstractCraftsman


class NextAction:
    action_type: ActionType
    position: Position
    craftsman: AbstractCraftsman

    def __init__(self, craftsman: AbstractCraftsman, action_type: ActionType, position: Position):
        self.craftsman = craftsman
        self.action_type = action_type
        self.position = position
