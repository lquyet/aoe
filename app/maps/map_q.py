import tkinter as tk
import scipy.stats as stats


from app.helpers.constants import MAX_NUM_OF_CELLS_IN_WIDTH, MAX_NUM_OF_CELLS_IN_HEIGHT, MAX_NUMBER_OF_OBJECT, \
    MIN_NUMBER_OF_OBJECT
from app.helpers.enums import Side
from app.helpers.utils import get_number_of_object
from app.maps.map import Map
from app.models import GameResp
from app.objects import CraftsmanA, CraftsmanB


class CustomMapForQ(Map):

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

    def init_map(self, data: GameResp):
        self.create_map_neutral()
        self.create_map_component(data=data)

    def flatten_map(self, side: Side):
        flatten_cells = self.get_flatten_cells(side=side)
        flatten_craftsmen = self.get_flatten_craftsmen(side=side)
        flatten_point = self.get_flatten_point(side=side)
        flatten_map_resp = flatten_cells + flatten_craftsmen + flatten_point
        return flatten_map_resp

    def get_flatten_cells(self, side: Side):
        flatten_cells = []
        for cell_row in self._cells:
            for cell in cell_row:
                flatten_cells.append(get_number_of_object(obj=cell, side=side))
            for j in range(MAX_NUM_OF_CELLS_IN_WIDTH - self._number_of_cells_in_width):
                flatten_cells.append(0)
        for i in range(MAX_NUM_OF_CELLS_IN_HEIGHT - self._number_of_cells_in_height):
            for j in range(MAX_NUM_OF_CELLS_IN_WIDTH - self._number_of_cells_in_width):
                flatten_cells.append(0)
        for i in range(len(flatten_cells)):
            mean = (MAX_NUMBER_OF_OBJECT + MIN_NUMBER_OF_OBJECT) / 2
            difference = MAX_NUMBER_OF_OBJECT - MIN_NUMBER_OF_OBJECT
            flatten_cells[i] = (flatten_cells[i] - mean) / difference
        return flatten_cells

    def get_flatten_craftsmen(self, side: Side):
        flatten_craftsmen = []
        for craftsman in self.craftsmen:
            if (type(craftsman) is CraftsmanA and side == Side.A) or (type(craftsman) is CraftsmanB and side == Side.B):
                new_item = craftsman.position.x * MAX_NUM_OF_CELLS_IN_WIDTH + craftsman.position.y
                flatten_craftsmen.append(new_item)
        for craftsman in self.craftsmen:
            if (type(craftsman) is CraftsmanA and side == Side.B) or (type(craftsman) is CraftsmanB and side == Side.A):
                new_item = craftsman.position.x * MAX_NUM_OF_CELLS_IN_WIDTH + craftsman.position.y
                flatten_craftsmen.append(new_item)
        for i in range(len(flatten_craftsmen)):
            mean = (MAX_NUM_OF_CELLS_IN_WIDTH * MAX_NUM_OF_CELLS_IN_HEIGHT) / 2
            difference = MAX_NUM_OF_CELLS_IN_WIDTH * MAX_NUM_OF_CELLS_IN_HEIGHT
            flatten_craftsmen[i] = (flatten_craftsmen[i] - mean) / difference
        return flatten_craftsmen

    def get_flatten_point(self, side: Side):
        point_a, point_b = self.calculate_point()
        if side == Side.A:
            flatten_point = point_a - point_b
        else:
            flatten_point = point_b - point_a
        flatten_point = flatten_point / (self._number_of_cells_in_width * self._number_of_cells_in_height * 2)
        return [flatten_point]

