from app.helpers.enums import ActionType, MoveType, BuildAndDestroyType, Direction
from app.objects import Position


def mapping_from_key_list_to_action_type(action: ActionType, key_list: list):
    if action is ActionType.MOVE:
        if "Left" in key_list:
            if "Up" in key_list:
                return MoveType.UPPER_LEFT
            if "Down" in key_list:
                return MoveType.LOWER_LEFT
            return MoveType.LEFT
        if "Right" in key_list:
            if "Up" in key_list:
                return MoveType.UPPER_RIGHT
            if "Down" in key_list:
                return MoveType.LOWER_RIGHT
            return MoveType.RIGHT
        if "Up" in key_list:
            return MoveType.UP
        if "Down" in key_list:
            return MoveType.DOWN
    elif action is ActionType.BUILD or action is ActionType.DESTROY:
        if "Left" in key_list:
            return BuildAndDestroyType.LEFT
        if "Right" in key_list:
            return BuildAndDestroyType.RIGHT
        if "Up" in key_list:
            return BuildAndDestroyType.ABOVE
        if "Down" in key_list:
            return BuildAndDestroyType.BELOW
    else:
        return None


def new_position_from_direction(current_pos: Position, direction: Direction) -> Position:
    mapping_direction_and_vector = {
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
        Direction.UP: (0, - 1),
        Direction.DOWN: (0, 1),
        Direction.UPPER_LEFT: (-1, -1),
        Direction.LOWER_LEFT: (-1, 1),
        Direction.UPPER_RIGHT: (1, -1),
        Direction.LOWER_RIGHT: (1, 1)
    }
    vector = mapping_direction_and_vector.get(direction)
    new_pos = Position(
        x=current_pos.x + vector[0],
        y=current_pos.y + vector[1]
    )
    return new_pos


DIRECTION_CAN_BUILD_AND_DESTROY = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
DIRECTION_CAN_MOVE = [Direction.UPPER_LEFT, Direction.UPPER_RIGHT, Direction.LOWER_LEFT, Direction.LOWER_RIGHT,
                      Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]


MAPPING_BUILD_AND_DESTROY_TYPE_TO_DIRECTION = {
    BuildAndDestroyType.LEFT: Direction.LEFT,
    BuildAndDestroyType.RIGHT: Direction.RIGHT,
    BuildAndDestroyType.ABOVE: Direction.UP,
    BuildAndDestroyType.BELOW: Direction.DOWN,
}
MAPPING_MOVE_TYPE_TO_DIRECTION = {}
for move_type in MoveType:
    MAPPING_MOVE_TYPE_TO_DIRECTION[move_type] = Direction(move_type)
