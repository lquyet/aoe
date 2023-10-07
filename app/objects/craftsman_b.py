from app.objects import AbstractCraftsman, Position


class CraftsmanB(AbstractCraftsman):

    def __init__(self, position: Position, craftsman_id: str):
        super().__init__(position=position, craftsman_id=craftsman_id, image_path="../images/craftsman_b.png")
