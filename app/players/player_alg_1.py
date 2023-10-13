from app.helpers.constants import INIT_WIDTH, INIT_HEIGHT, INFO_BOARD_WIDTH
from app.helpers.enums import ActionType, Side
from app.helpers.utils import new_position_from_direction, DIRECTION_CAN_BUILD_AND_DESTROY, \
    convert_next_action_to_child_action_req
from app.map_controller import MapController
from app.maps.map_alg_1 import CustomMapForAlg1
from app.models import GameResp
from app.objects import AbstractCraftsman, CraftsmanA, CraftsmanB
from app.schemas import NextAction


class PlayerAlgorithm1(MapController):
    """
        Player với thuật toán 1: trâu bò
        Các Craftsmen sẽ di chuyển tới Castle (không nằm trong territory) gần nhất
        Trong quá trình di chuyển, xây 4 bức tường xung quanh chúng
        Nếu không có Castle, chọn ngẫu nhiên một ô (không nằm trong territory) có thể tới được
    """
    _my_map: CustomMapForAlg1

    def init_map(self, data: GameResp):
        window_width = INIT_WIDTH
        window_height = INIT_HEIGHT

        if self._frame:
            self._frame.config(width=window_width, height=window_height)
        if self._canvas:
            self._canvas.config(width=window_width - INFO_BOARD_WIDTH, height=window_height)

        self._my_map = CustomMapForAlg1(canvas=self._canvas,
                                        number_of_cells_in_width=data.field.width,
                                        number_of_cells_in_height=data.field.height,
                                        map_width=window_width-INFO_BOARD_WIDTH,
                                        map_height=window_height)
        self._my_map.init_map(data=data)
        my_type_of_craftsmen = CraftsmanA if self._side is Side.A else CraftsmanB
        self._my_craftsmen = [craftsman for craftsman in self._my_map.craftsmen
                              if type(craftsman) is my_type_of_craftsmen]

    def think(self):
        self._request_data.actions = []
        next_actions = []
        for craftsman in self._my_craftsmen:
            next_actions.append(self.get_next_action_for_craftsman(craftsman=craftsman))
        for action in next_actions:
            self._request_data.actions.append(
                convert_next_action_to_child_action_req(action=action)
            )

    def get_next_action_for_craftsman(self, craftsman: AbstractCraftsman) -> NextAction:
        for direction in DIRECTION_CAN_BUILD_AND_DESTROY:
            build_pos = new_position_from_direction(current_pos=craftsman.position, direction=direction)
            if not self._my_map.check_if_position_is_valid(position=build_pos):
                continue
            if self._my_map.check_if_pos_is_close_territory(pos=build_pos, side=self._side):
                continue
            if self._my_map.check_if_craftsman_can_build(build_position=build_pos):
                return NextAction(craftsman=craftsman, action_type=ActionType.BUILD, position=build_pos)
        next_move_pos = self._my_map.get_best_position_to_move(craftsman=craftsman, side=self._side)
        if next_move_pos == craftsman.position:
            return NextAction(craftsman=craftsman, action_type=ActionType.STAY, position=next_move_pos)
        else:
            return NextAction(craftsman=craftsman, action_type=ActionType.MOVE, position=next_move_pos)
