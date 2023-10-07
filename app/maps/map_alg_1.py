import queue
import random
import tkinter as tk
from typing import List

from app.helpers.constants import MAX_DISTANCE
from app.helpers.enums import Side
from app.helpers.utils import DIRECTION_CAN_MOVE, new_position_from_direction
from app.maps.map import Map
from app.models import GameResp
from app.objects import AbstractCraftsman, AbstractObject, Position, Castle, WallA, WallB


class CustomMapForAlg1(Map):
    _point: List[List[int]]
    _is_reached: List[List[int]]
    _calculate_distance_queue: queue.Queue
    _is_available_castle: bool
    _mapping_from_craftsman_id_to_target: dict

    def __init__(self,
                 map_width: int,
                 map_height: int,
                 number_of_cells_in_width: int,
                 number_of_cells_in_height: int,
                 canvas: tk.Canvas):
        super().__init__(map_width=map_width,
                         map_height=map_height,
                         number_of_cells_in_width=number_of_cells_in_width,
                         number_of_cells_in_height=number_of_cells_in_height,
                         canvas=canvas)
        self._point = []
        self._is_reached = []
        self._calculate_distance_queue = queue.Queue()
        self._mapping_from_craftsman_id_to_target = {}

    def init_map(self, data: GameResp):
        self.create_map_neutral()
        self.create_map_component(data=data)
        self.setup_target_mapping()

    def setup_target_mapping(self):
        for craftsman in self.craftsmen:
            self._mapping_from_craftsman_id_to_target[craftsman.craftsman_id] = craftsman.position

    def get_best_position_to_move(self, craftsman: AbstractCraftsman, side: Side) -> Position:
        self._is_reached = [[
            False
            for y in range(self._number_of_cells_in_height)]
            for x in range(self._number_of_cells_in_width)]
        self._is_checked = [[
            False
            for y in range(self._number_of_cells_in_height)]
            for x in range(self._number_of_cells_in_width)]
        self.dfs_from_craftsman(craftsman_pos=craftsman.position, current_pos=craftsman.position, side=side)
        new_target_pos = self.select_target(craftsman=craftsman)
        self._mapping_from_craftsman_id_to_target[craftsman.craftsman_id] = new_target_pos
        self.calculate_distance_from_cur_pos_to_all_cell(current_pos=new_target_pos, side=side)
        min_move_pos = craftsman.position
        current_point = MAX_DISTANCE
        for direction in DIRECTION_CAN_MOVE:
            move_pos = new_position_from_direction(current_pos=craftsman.position, direction=direction)
            if not self.check_if_craftsman_can_move(move_pos=move_pos, craftsman_side=side):
                continue
            if current_point > self._point[move_pos.x][move_pos.y]:
                current_point = self._point[move_pos.x][move_pos.y]
                min_move_pos = move_pos
        return min_move_pos

    def select_target(self, craftsman: AbstractCraftsman):
        cur_target_pos = self._mapping_from_craftsman_id_to_target.get(craftsman.craftsman_id)
        if cur_target_pos != craftsman.position and self._is_reached[cur_target_pos.x][cur_target_pos.y]:
            return cur_target_pos
        for castle in self.castles:
            if self.check_if_pos_is_close_territory(pos=castle.position, side=Side.A):
                continue
            if self.check_if_pos_is_close_territory(pos=castle.position, side=Side.B):
                continue
            if not self._is_reached[castle.position.x][castle.position.y]:
                continue
            return castle.position
        available_cells = []
        for cell_row in self._cells:
            for cell in cell_row:
                if self._is_reached[cell.position.x][cell.position.y] and cell.position != craftsman.position:
                    available_cells.append(cell)
        return random.choice(available_cells).position

    def calculate_distance_from_cur_pos_to_all_cell(self, current_pos: Position, side: Side):
        self._point = [[
            MAX_DISTANCE
            for y in range(self._number_of_cells_in_height)]
            for x in range(self._number_of_cells_in_width)]
        self._point[current_pos.x][current_pos.y] = 0
        self.bfs_calculate_distance(current_pos=current_pos, side=side)

    def bfs_calculate_distance(self, current_pos: Position, side: Side):
        self._calculate_distance_queue.put(current_pos)
        while not self._calculate_distance_queue.empty():
            current_pos = self._calculate_distance_queue.get()
            for direction in DIRECTION_CAN_MOVE:
                new_pos = new_position_from_direction(current_pos=current_pos, direction=direction)
                if not self.check_if_craftsman_can_move(move_pos=new_pos, craftsman_side=side):
                    continue
                if self._point[new_pos.x][new_pos.y] > self._point[current_pos.x][current_pos.y] + 1:
                    self._point[new_pos.x][new_pos.y] = self._point[current_pos.x][current_pos.y] + 1
                    self._calculate_distance_queue.put(new_pos)

    def dfs_from_craftsman(self, craftsman_pos: Position, current_pos: Position, side: Side):
        x = current_pos.x
        y = current_pos.y
        if self._is_checked[x][y]:
            return
        self._is_checked[x][y] = True
        for craftsman in self.craftsmen:
            if craftsman.position == current_pos and craftsman_pos != current_pos:
                return
        if type(self._cells[x][y]) is WallB and side == Side.A:
            return
        if type(self._cells[x][y]) is WallA and side == Side.B:
            return
        self._is_reached[x][y] = True
        for direction in DIRECTION_CAN_MOVE:
            new_pos = new_position_from_direction(current_pos=current_pos, direction=direction)
            if not self.check_if_craftsman_can_move(move_pos=new_pos, craftsman_side=side):
                continue
            self.dfs_from_craftsman(craftsman_pos=craftsman_pos, current_pos=new_pos, side=side)
