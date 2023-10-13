import os

import requests
from dotenv import load_dotenv

from app.config import settings
from models import GameActionsReq, GameActionsResp, GameStatusResp, GameResp

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
load_dotenv(os.path.join(BASE_DIR, '../.env'))


class Service:

    def __init__(self):
        self._game_id = settings.GAME_ID
        self._url = settings.URL
        self._token = settings.TOKEN
        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': self._token
        }

    def get_game_with_game_id(self) -> GameResp:
        response = requests.get(self._url + f"/games/{self._game_id}",
                                headers=self._headers)
        return GameResp(**response.json())

    def get_game_status_with_game_id(self) -> GameStatusResp:
        response = requests.get(self._url + f"/games/{self._game_id}/status",
                                headers=self._headers)
        return GameStatusResp(**response.json())

    def get_game_actions_with_game_id(self) -> list[GameActionsResp]:
        response = requests.get(self._url + f"/games/{self._game_id}/actions",
                                headers=self._headers)
        list_resp = []
        if type(response.json()) is list:
            for actions in response.json():
                list_resp.append(GameActionsResp(**actions))
        return list_resp

    def post_game_actions(self, game_actions_req: GameActionsReq) -> int:
        data = game_actions_req.dict()
        response = requests.post(self._url + f"/games/{self._game_id}/actions",
                                 json=data,
                                 headers=self._headers)
        return response.status_code
