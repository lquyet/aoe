from app.objects import AbstractCraftsman, Position


class CraftsmanA(AbstractCraftsman):

    def __init__(self, position: Position, craftsman_id: str):
        super().__init__(position=position, craftsman_id=craftsman_id, image_path="../images/craftsman_a.png")
