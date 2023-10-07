import os
import tkinter as tk

from dotenv import load_dotenv

from app.helpers.enums import Side, ActionType
from app.helpers.utils import new_position_from_direction, MAPPING_BUILD_AND_DESTROY_TYPE_TO_DIRECTION, \
    MAPPING_MOVE_TYPE_TO_DIRECTION
from app.models import GameResp, GameActionsResp
from app.objects import AbstractObject, Neutral, Position, Castle, CraftsmanA, CraftsmanB, Pond, \
    AbstractCraftsman, WallA, WallB
from app.schemas import NextAction

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
load_dotenv(os.path.join(BASE_DIR, '../../.env'))


class Map:
    _map_width: int
    _map_height: int
    _number_of_cells_in_width: int
    _number_of_cells_in_height: int
    _cell_width: int
    _cell_height: int
    _canvas: tk.Canvas
    _cells: list[list[AbstractObject]]
    _castle_point: int
    _territory_point: int
    _wall_point: int
    _chosen_craftsman_pos: Position
    craftsmen: list[AbstractCraftsman]
    castles: list[Castle]

    def __init__(self,
                 map_width: int,
                 map_height: int,
                 number_of_cells_in_width: int,
                 number_of_cells_in_height: int,
                 canvas: tk.Canvas):
        self._map_width: int = map_width
        self._map_height: int = map_height
        self._number_of_cells_in_width: int = number_of_cells_in_width
        self._number_of_cells_in_height: int = number_of_cells_in_height
        self._cell_width = int(map_width / number_of_cells_in_width)
        self._cell_height = int(map_height / number_of_cells_in_height)
        self._canvas = canvas
        self._cells: list[list[AbstractObject]] = []
        self.craftsmen: list[AbstractCraftsman] = []
        self._castle_point = 0
        self._territory_point = 0
        self._wall_point = 0
        self._chosen_craftsman_pos = Position(x=0, y=0)
        self._is_checked = []
        self.castles = []

    def display(self):
        for cell_row in self._cells:
            for cell in cell_row:
                cell.display(
                    rect_width=self._cell_width, rect_height=self._cell_height, canvas=self._canvas
                )
        for craftsman in self.craftsmen:
            craftsman.display(
                rect_width=self._cell_width, rect_height=self._cell_height, canvas=self._canvas
            )

    def init_map(self, data: GameResp):
        self.create_map_neutral()
        self.create_map_component(data=data)

    def create_map_neutral(self):
        self._cells = [[
            Neutral(position=Position(x=x, y=y))
            for y in range(self._number_of_cells_in_height)]
            for x in range(self._number_of_cells_in_width)]

    def create_map_component(self, data: GameResp):
        if data is None or data.field is None:
            return
        self._castle_point = data.field.castle_coeff
        self._territory_point = data.field.territory_coeff
        self._wall_point = data.field.wall_coeff

        for castle in data.field.castles:
            new_castle = Castle(position=Position(x=castle.x, y=castle.y))
            self._cells[castle.x][castle.y] = new_castle
            self.castles.append(new_castle)
        for pond in data.field.ponds:
            self._cells[pond.x][pond.y] = Pond(position=Position(x=pond.x, y=pond.y))
        for craftsman in data.field.craftsmen:
            if craftsman.side == Side.A:
                self.craftsmen.append(CraftsmanA(position=Position(x=craftsman.x, y=craftsman.y),
                                                 craftsman_id=craftsman.id))
            if craftsman.side == Side.B:
                self.craftsmen.append(CraftsmanB(position=Position(x=craftsman.x, y=craftsman.y),
                                                 craftsman_id=craftsman.id))

    def change_map_component_from_actions_response(self, child_action: GameActionsResp.ChildAction):
        for craftsman in self.craftsmen:
            if craftsman.craftsman_id == child_action.craftsman_id:
                if child_action.action == ActionType.MOVE:
                    move_pos = new_position_from_direction(
                        current_pos=craftsman.position,
                        direction=MAPPING_MOVE_TYPE_TO_DIRECTION.get(child_action.action_param)
                    )
                    self.handle_move_action(craftsman=craftsman, move_pos=move_pos)
                if child_action.action == ActionType.BUILD:
                    build_pos = new_position_from_direction(
                        current_pos=craftsman.position,
                        direction=MAPPING_BUILD_AND_DESTROY_TYPE_TO_DIRECTION.get(child_action.action_param)
                    )
                    self.handle_build_action(craftsman=craftsman, valid_build_pos=build_pos)
                if child_action.action == ActionType.DESTROY:
                    destroy_pos = new_position_from_direction(
                        current_pos=craftsman.position,
                        direction=MAPPING_BUILD_AND_DESTROY_TYPE_TO_DIRECTION.get(child_action.action_param)
                    )
                    self.handle_destroy_action(craftsman=craftsman, destroy_pos=destroy_pos)

    def handle_move_action(self, craftsman: AbstractCraftsman, valid_move_pos: Position):
        craftsman.position = valid_move_pos
        craftsman.raise_rectangle(canvas=self._canvas)

    def handle_action(self, next_action: NextAction):
        if next_action.action_type == ActionType.MOVE:
            self.handle_move_action(craftsman=next_action.craftsman, valid_move_pos=next_action.position)
        if next_action.action_type == ActionType.BUILD:
            self.handle_build_action(craftsman=next_action.craftsman, valid_build_pos=next_action.position)
        if next_action.action_type == ActionType.DESTROY:
            self.handle_destroy_action(valid_destroy_pos=next_action.position)

    def handle_build_action(self, craftsman: AbstractCraftsman, valid_build_pos: Position):
        if type(craftsman) is CraftsmanA:
            self._cells[valid_build_pos.x][valid_build_pos.y] = WallA(position=valid_build_pos)
        else:
            self._cells[valid_build_pos.x][valid_build_pos.y] = WallB(position=valid_build_pos)

    def handle_destroy_action(self, valid_destroy_pos: Position):
        self._cells[valid_destroy_pos.x][valid_destroy_pos.y] = Neutral(position=valid_destroy_pos)

    def check_if_position_has_craftsman(self, position: Position) \
            -> bool:
        for craftsman in self.craftsmen:
            if craftsman.position.x == position.x and craftsman.position.y == position.y:
                return True
        return False

    def resize(self, map_width: int, map_height: int):
        self._map_width = map_width
        self._map_height = map_height
        self._cell_width = int(map_width / self._number_of_cells_in_width)
        self._cell_height = int(map_height / self._number_of_cells_in_height)
        for cell_row in self._cells:
            for cell in cell_row:
                cell.display_when_having_resize_event(
                    rect_width=self._cell_width, rect_height=self._cell_height, canvas=self._canvas
                )

        for craftsman in self.craftsmen:
            craftsman.display_when_having_resize_event(
                rect_width=self._cell_width, rect_height=self._cell_height, canvas=self._canvas
            )
            craftsman.raise_rectangle(canvas=self._canvas)

    def delete(self):
        self.reset()
        for cell_row in self._cells:
            for cell in cell_row:
                cell.delete(canvas=self._canvas)
        for craftsman in self.craftsmen:
            craftsman.delete(canvas=self._canvas)

    def reset(self):
        for craftsman in self.craftsmen:
            craftsman.remove_border(canvas=self._canvas)
            craftsman.remove_wrapper(canvas=self._canvas)
            craftsman.is_played = False

    def choose_craftsman(self, side: Side):
        if self.check_if_all_craftsmen_is_played(side=side):
            for craftsman in self.craftsmen:
                craftsman.is_played = False
        for craftsman in self.craftsmen:
            if side == Side.A and type(craftsman) is CraftsmanA or side == Side.B and type(craftsman) is CraftsmanB:
                if not craftsman.is_played:
                    craftsman.display_border(rect_width=self._cell_width, rect_height=self._cell_height,
                                             canvas=self._canvas)
                    craftsman.is_played = True
                    self._chosen_craftsman_pos = craftsman.position
                    return craftsman

    def check_if_all_craftsmen_is_played(self, side: Side):
        for craftsman in self.craftsmen:
            if side == Side.A and type(craftsman) is CraftsmanA or side == Side.B and type(craftsman) is CraftsmanB:
                craftsman.is_played = False

    def choose_direction(self, key_list: list):
        next_move_pos_x = self._chosen_craftsman_pos.x
        next_move_pos_y = self._chosen_craftsman_pos.y

        if "Left" in key_list:
            next_move_pos_x -= 1
        if "Right" in key_list:
            next_move_pos_x += 1
        if "Up" in key_list:
            next_move_pos_y -= 1
        if "Down" in key_list:
            next_move_pos_y += 1

        if 0 <= next_move_pos_x < self._number_of_cells_in_width - 1 \
                and 0 <= next_move_pos_y < self._number_of_cells_in_height - 1:
            self._cells[next_move_pos_x][next_move_pos_y].change_color(canvas=self._canvas)
            self._cells[next_move_pos_x][next_move_pos_y].raise_rectangle(canvas=self._canvas)
            self.update_queue(position=self._cells[next_move_pos_x][next_move_pos_y].position)
            self.revert_neighbor_color(x=self._chosen_craftsman_pos.x, y=self._chosen_craftsman_pos.y)

    def update_queue(self, position: Position):
        self._queue.put(position)
        if self._queue.qsize() > len(self.craftsmen) / 2:
            self._queue.get()

    def remove_border_of_craftsman(self):
        for craftsman in self.craftsmen:
            craftsman.delete_border(canvas=self._canvas)

    def revert_neighbor_color(self, x: int, y: int):
        border_list = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for (i, j) in border_list:
            if 0 <= x + i < self._width and 0 <= y + j < self._height:
                is_change_color = True
                queue_current_size = self._queue.qsize()
                for index in range(0, queue_current_size):
                    item = self._queue.get()
                    if item.x == self._point[x + i][y + j].position.x and \
                            item.y == self._point[x + i][y + j].position.y:
                        is_change_color = False
                    self._queue.put(item)
                if is_change_color:
                    self._point[x + i][y + j].revert_color(self._canvas)

    def get_actual_position(self, position: Position, window_width: int, window_height: int):
        rect_width = int(window_width / self._width)
        rect_height = int(window_height / self._height)
        return position.x * rect_width, position.y * rect_height

    def update_choose_action_on_craftsman(self, craftsman: AbstractObject, action_type: ActionType,
                                          window_width: int, window_height: int):
        rect_width = int(window_width / self._width)
        rect_height = int(window_height / self._height)
        x1 = craftsman.position.x * rect_width
        y1 = craftsman.position.y * rect_height
        x2 = x1 + rect_width
        y2 = y1 + rect_height
        craftsman.choose_action(canvas=self._canvas, action_type=action_type,
                                x1=x1, x2=x2, y1=y1, y2=y2)

    def calculate_point(self) -> (int, int):
        point_a = 0
        point_b = 0

        for row in self._point:
            for square in row:
                if type(square) is WallA:
                    point_a += self._wall_point
                if type(square) is WallB:
                    point_b += self._wall_point
                if square.is_close_territory_a or square.is_open_territory_a:
                    if type(square) is Castle:
                        point_a += self._castle_point
                    else:
                        point_a += self._territory_point
                if square.is_close_territory_b or square.is_open_territory_b:
                    if type(square) is Castle:
                        point_b += self._castle_point
                    else:
                        point_b += self._territory_point

        return point_a, point_b

    def update_territory_status(self):
        for row in self._point:
            for square in row:
                is_close_territory_a = self.check_if_pos_is_close_territory(square.position, side=Side.A)
                is_close_territory_b = self.check_if_pos_is_close_territory(square.position, side=Side.B)
                if is_close_territory_a and is_close_territory_b:
                    square.is_close_territory_a = True
                    square.is_close_territory_b = True
                    square.is_open_territory_a = False
                    square.is_open_territory_b = False
                elif is_close_territory_a:
                    square.is_close_territory_a = True
                    square.is_close_territory_b = False
                    square.is_open_territory_a = False
                    square.is_open_territory_b = False
                elif is_close_territory_b:
                    square.is_close_territory_a = False
                    square.is_close_territory_b = True
                    square.is_open_territory_a = False
                    square.is_open_territory_b = False
                else:
                    if square.is_close_territory_a:
                        square.is_close_territory_a = False
                        square.is_close_territory_b = False
                        square.is_open_territory_a = True
                        square.is_open_territory_b = False
                    if square.is_close_territory_b:
                        square.is_close_territory_a = False
                        square.is_close_territory_b = False
                        square.is_open_territory_a = False
                        square.is_open_territory_b = True

    def check_if_pos_is_close_territory(self, pos: Position, side: Side):
        if type(pos) is WallA and side == Side.A:
            return False
        if type(pos) is WallB and side == Side.B:
            return False
        self._is_checked = [[
            False
            for y in range(self._number_of_cells_in_height)]
            for x in range(self._number_of_cells_in_width)]
        return self.dfs_check_close_territory(pos=pos, side=side)

    def dfs_check_close_territory(self, pos: Position, side: Side):
        x = pos.x
        y = pos.y
        if self._is_checked[x][y]:
            return True
        self._is_checked[x][y] = True
        if type(self._cells[x][y]) is WallA and side == Side.A:
            return True
        if type(self._cells[x][y]) is WallB and side == Side.B:
            return True
        if x == 0 or y == 0 \
                or x == self._number_of_cells_in_width-1 or y == self._number_of_cells_in_height-1:
            return False
        if not self.dfs_check_close_territory(pos=self._cells[x - 1][y].position, side=side):
            return False
        if not self.dfs_check_close_territory(pos=self._cells[x][y - 1].position, side=side):
            return False
        if not self.dfs_check_close_territory(pos=self._cells[x + 1][y].position, side=side):
            return False
        if not self.dfs_check_close_territory(pos=self._cells[x][y + 1].position, side=side):
            return False
        return True

    def check_if_craftsman_can_build(self, build_position: Position):
        if not self.check_if_position_is_valid(position=build_position):
            return False
        for craftsman in self.craftsmen:
            if craftsman.position == build_position:
                return False
        for cell_row in self._cells:
            for cell in cell_row:
                if cell.position == build_position:
                    if type(cell) in [WallA, WallB, Castle]:
                        return False
                    return True
        return False

    def check_if_craftsman_can_move(self, move_pos: Position, craftsman_side: Side):
        if not self.check_if_position_is_valid(position=move_pos):
            return False
        for craftsman in self.craftsmen:
            if craftsman.position == move_pos:
                return False
        for cell_row in self._cells:
            for cell in cell_row:
                if cell.position == move_pos:
                    type_of_opponent_wall = WallB if craftsman_side is Side.A else WallA
                    if type(cell) in [type_of_opponent_wall, Pond]:
                        return False
                    return True
        return False

    def check_if_position_is_valid(self, position: Position):
        if position.x < 0 or position.x > self._number_of_cells_in_width - 1:
            return False
        if position.y < 0 or position.y > self._number_of_cells_in_height - 1:
            return False
        return True
