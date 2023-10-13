import json

from app.models import GameResp, GameStatusResp, GameActionsReq, GameActionsResp
from app.services import Service

action_lists = []
current_turn = 0
count_post_request = 0


class MockService(Service):

    def __init__(self, team_id: int):
        super().__init__()
        self._team_id = team_id

    def get_game_with_game_id(self) -> GameResp:
        raw_data = open("mock/map_mock.json")
        response: dict = json.load(raw_data)
        return GameResp(**response)

    def get_game_status_with_game_id(self) -> GameStatusResp:
        raw_data = open("mock/game_status_mock.json")
        data: dict = json.load(raw_data)
        global current_turn
        response = {
            "cur_turn": current_turn,
            "max_turn": data.get("max_turn"),
            "remaining": data.get("remaining")
        }
        return GameStatusResp(**response)

    def get_game_actions_with_game_id(self) -> list[GameActionsResp]:
        global action_lists
        list_resp = []
        if type(action_lists) is list:
            for actions in action_lists:
                list_resp.append(GameActionsResp(**actions))
        return list_resp

    def post_game_actions(self, game_actions_req: GameActionsReq) -> int:
        data = game_actions_req.dict()
        data["team_id"] = self._team_id
        global action_lists
        global current_turn
        global count_post_request
        action_lists.append(data)
        count_post_request += 1
        if current_turn == 0 and count_post_request == 2:
            count_post_request = 0
            current_turn += 1
        elif current_turn > 0 and count_post_request == 2:
            count_post_request = 0
            current_turn += 1
        return 200
