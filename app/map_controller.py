import copy
import json
import time
import tkinter as tk
from typing import List

from app.helpers.constants import INIT_WIDTH, INFO_BOARD_WIDTH, INIT_HEIGHT
from app.helpers.enums import Side, ActionType, MoveType
from app.maps.map import Map
from app.mock.mock_service import MockService
from app.objects import CraftsmanA, CraftsmanB, AbstractCraftsman
from models import GameActionsReq, GameResp, GameActionsResp
from services import Service


class MapController:

    def __init__(self, window: tk.Tk, frame: tk.Frame, canvas: tk.Canvas, team_id: int):
        self._window: tk.Tk = window
        self._window_width = self._window.winfo_width() if self._window else None
        self._window_height = self._window.winfo_height() if self._window_width else None
        self._frame: tk.Frame = frame
        self._canvas: tk.Canvas = canvas

        self._services: Service = MockService(team_id=team_id)

        self._team_id: int = team_id

        self._new_action: GameActionsReq.ChildAction = GameActionsReq.ChildAction(action=ActionType.MOVE,
                                                                                  action_param=MoveType.LEFT,
                                                                                  crafts_man_id="1")
        self._side: Side = Side.A
        self._side_text: tk.Label = tk.Label(self._frame, text="Side: A", font=("Arial", 12))

        self._cur_turn: int = 0
        self._cur_turn_text: tk.Label = tk.Label(self._frame, text=f"Turn: {self._cur_turn}", font=("Arial", 12))

        self._my_next_turn: int = 0
        self._my_next_turn_text: tk.Label = tk.Label(self._frame, text=f"Turn: {self._cur_turn}", font=("Arial", 12))

        self._time_remain: int = 30
        self._time_remain_text: tk.Label = tk.Label(self._frame, text=f"Time remaining: {self._time_remain}",
                                                    font=("Arial", 12))

        self._request_data: GameActionsReq = GameActionsReq(turn=1, actions=[])
        self._request_data_text: tk.Text = tk.Text(self._frame, font=("Courier New", 10), width=100, height=15)

        self._send_request_button: tk.Button = tk.Button(frame, text="Send data", command=self.send_data)

        self._is_send_data = False

        self._response_text: tk.Label = tk.Label(self._frame, text="Response", font=("Arial", 12))

        self._point_text: tk.Label = tk.Label(self._frame, text="A:0 B:0", font=("Arial", 12))

        self._my_map: Map = None

        self._my_craftsmen: list[AbstractCraftsman] = []

    def create_map(self):
        data = self._services.get_game_with_game_id()
        list_actions = self._services.get_game_actions_with_game_id()
        status_data = self._services.get_game_status_with_game_id()
        should_retry = True
        while should_retry:
            if status_data.cur_turn is None and status_data.max_turn is None and status_data.remaining is None:
                time.sleep(0.5)
                print("retry")
                continue
            should_retry = False

        for side in data.sides:
            if side.team_id == self._team_id:
                self._side = side.side
        self._side_text.config(text=f"Side: {self._side}")

        self._cur_turn = status_data.cur_turn
        self._cur_turn_text.config(text=f"Turn: {str(self._cur_turn)}")
        self.configure_my_next_turn()
        self._request_data.turn = self._my_next_turn

        self.create_map_from_server(data=data, list_actions=list_actions)

        (point_a, point_b) = self._my_map.calculate_point()
        self._point_text.config(text=f"A:{point_a} B:{point_b}")

        data = self._request_data.dict()
        pretty_json = json.dumps(data, indent=1)
        self._request_data_text.delete("1.0", tk.END)
        self._request_data_text.insert(tk.END, pretty_json)
        self._time_remain = status_data.remaining

    def configure_my_next_turn(self):
        self._my_next_turn = self._cur_turn + 1
        if self._side is Side.A and self._my_next_turn % 2 == 1:
            self._my_next_turn += 1
        if self._side is Side.B and self._my_next_turn % 2 == 0:
            self._my_next_turn += 1

    def create_map_from_server(self, data: GameResp, list_actions: List[GameActionsResp]):
        if self._my_map:
            self._my_map.delete()
        self.init_map(data)

        list_actions = self.clean_list_game_action_resp(list_actions)

        for i in range(0, len(list_actions)):
            if self._cur_turn >= list_actions[i].turn and i == len(list_actions) - 1 or \
                    self._cur_turn >= list_actions[i].turn != list_actions[i + 1].turn:
                self._my_map.change_map_component_from_actions_response(list_actions=list_actions[i].actions)

    def clean_list_game_action_resp(self, list_actions: list[GameActionsResp]) -> list[GameActionsResp]:
        m = {}
        r = []
        for action in list_actions:
            m[action.turn] = action

        t = dict(sorted(m.items()))

        for key in t.keys():
            r.append(t[key])
        return r

    def init_map(self, data: GameResp):
        window_width = INIT_WIDTH
        window_height = INIT_HEIGHT

        if self._frame:
            self._frame.config(width=window_width, height=window_height)
        if self._canvas:
            self._canvas.config(width=window_width - INFO_BOARD_WIDTH, height=window_height)

        self._my_map = Map(canvas=self._canvas,
                           number_of_cells_in_width=data.field.width,
                           number_of_cells_in_height=data.field.height,
                           map_width=window_width-INFO_BOARD_WIDTH,
                           map_height=window_height
                           )
        self._my_map.init_map(data=data)
        my_type_of_craftsmen = CraftsmanA if self._side is Side.A else CraftsmanB
        self._my_craftsmen = [craftsman for craftsman in self._my_map.craftsmen
                              if type(craftsman) is my_type_of_craftsmen]

    def display_map(self):
        self._my_map.display()
        self._frame.config(width=self._window_width, height=self._window_height)
        self._canvas.config(width=self._window_width-INFO_BOARD_WIDTH, height=self._window_height)
        self._side_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=50)
        self._side_text.pack()
        self._cur_turn_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=100)
        self._cur_turn_text.pack()
        self._my_next_turn_text.place(x=self._window_width-INFO_BOARD_WIDTH+50, y=100)
        self._my_next_turn_text.pack()
        self._time_remain_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=150)
        self._time_remain_text.pack()
        self._request_data_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=200)
        self._request_data_text.pack()
        self._send_request_button.place(x=self._window_width-INFO_BOARD_WIDTH, y=550)
        self._send_request_button.pack()
        self._response_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=600)
        self._response_text.pack()
        self._point_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=650)
        self._point_text.pack()

    def resize(self):
        self._window_width = self._window.winfo_width()
        self._window_height = self._window.winfo_height()
        self._frame.config(width=self._window_width, height=self._window_height)
        self._canvas.config(width=self._window_width-INFO_BOARD_WIDTH, height=self._window_height)
        if self._my_map:
            self._my_map.resize(map_width=self._window_width-INFO_BOARD_WIDTH, map_height=self._window_height)
        self._cur_turn_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=50)
        self._my_next_turn_text.place(x=self._window_width-INFO_BOARD_WIDTH+50, y=100)
        self._side_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=100)
        self._time_remain_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=150)
        self._request_data_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=200)
        self._send_request_button.place(x=self._window_width-INFO_BOARD_WIDTH, y=550)
        self._response_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=600)
        self._point_text.place(x=self._window_width-INFO_BOARD_WIDTH, y=650)

    def refresh(self) -> int:
        if not self._is_send_data:
            self.think()
            self.send_data()
            self._is_send_data = True
        if self._time_remain is None:
            self._time_remain_text.config(text="Time remaining: None")
            return 1000
        if self._time_remain >= 1:
            self._time_remain -= 1
            self._time_remain_text.config(text=f"Time remaining: {self._time_remain}")
            return 1000
        elif self._time_remain < 1:
            status_data = self._services.get_game_status_with_game_id()
            if self._cur_turn < status_data.cur_turn:
                self._is_send_data = False
                self.update_map()
                return 200
            else:
                return 500

    def think(self):
        pass

    def update_map(self):
        data = self._services.get_game_with_game_id()
        list_actions = self._services.get_game_actions_with_game_id()
        status_data = self._services.get_game_status_with_game_id()

        self._cur_turn = status_data.cur_turn
        self._cur_turn_text.config(text=f"Turn: {str(self._cur_turn)}")
        self.configure_my_next_turn()
        self._request_data.turn = self._my_next_turn

        self.update_map_from_server(data=data, list_actions=list_actions)
        for side in data.sides:
            if side.team_id == self._team_id:
                self._side = side.side
        (point_a, point_b) = self._my_map.calculate_point()
        self._point_text.config(text=f"A:{point_a} B:{point_b}")

        data = self._request_data.dict()
        pretty_json = json.dumps(data, indent=1)
        self._request_data_text.delete("1.0", tk.END)
        self._request_data_text.insert(tk.END, pretty_json)
        self._time_remain = status_data.remaining

    def update_map_from_server(self, data: GameResp, list_actions: List[GameActionsResp]):
        if not self._my_map:
            self.init_map(data=data)

        if (self._side is Side.A and self._cur_turn % 2 == 0) or \
                (self._side is Side.B and self._cur_turn % 2 == 1):
            self._my_map.reset()
            self._request_data: GameActionsReq = GameActionsReq(turn=self._my_next_turn, actions=[])

        list_actions = self.clean_list_game_action_resp(list_actions)

        for i in range(0, len(list_actions)):
            if (self._cur_turn == list_actions[i].turn and i == len(list_actions) - 1) or \
                    (self._cur_turn == list_actions[i].turn and list_actions[i].turn != list_actions[i + 1].turn):
                self._my_map.change_map_component_from_actions_response(list_actions=list_actions[i].actions)

    def send_data(self):
        resp = self._services.post_game_actions(game_actions_req=self._request_data)
        self._response_text.config(text=str(resp))
