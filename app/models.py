import json
from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, root_validator

from app.helpers import enums
from app.helpers.enums import ActionType, MoveType, BuildAndDestroyType


class GameActionsReq(BaseModel):

    class ChildAction(BaseModel):
        action: Optional[ActionType]
        action_param: Optional[Union[MoveType, BuildAndDestroyType]]
        craftsman_id: Optional[str]

    turn: Optional[int]
    actions: Optional[List[ChildAction]]


class GameActionsResp(BaseModel):

    class ChildAction(BaseModel):
        action: Optional[ActionType]
        action_param: Optional[Union[MoveType, BuildAndDestroyType]]
        craftsman_id: Optional[str]
        id: Optional[int]
        action_id: Optional[int]

    turn: Optional[int]
    actions: Optional[List[ChildAction]]
    team_id: Optional[int]
    game_id: Optional[int]
    id: Optional[int]
    created_time: Optional[datetime]


class GameResp(BaseModel):

    class Side(BaseModel):
        side: Optional[enums.Side]
        team_name: Optional[str]
        team_id: Optional[int]
        game_id: Optional[int]
        id: Optional[int]

    class Field(BaseModel):

        class CastleResp(BaseModel):
            x: Optional[int]
            y: Optional[int]

        class CraftsMenResp(BaseModel):
            x: Optional[int]
            y: Optional[int]
            side: Optional[enums.Side]
            id: Optional[str]

        class PondResp(BaseModel):
            x: Optional[int]
            y: Optional[int]

        name: Optional[str]
        castle_coeff: Optional[int]
        wall_coeff: Optional[int]
        territory_coeff: Optional[int]
        id: Optional[int]
        width: Optional[int]
        height: Optional[int]
        ponds: Optional[Union[List[PondResp], str]]
        castles: Optional[Union[List[CastleResp], str]]
        craftsmen: Optional[Union[List[CraftsMenResp], str]]
        match_id: Optional[int]

        @root_validator()
        def validate_data(cls, data):
            if len(data.get("craftsmen")) > 0 and type(data.get("craftsmen")[0]) is cls.CraftsMenResp:
                return data
            castles = json.loads(data.get("castles"))
            craftsmen = json.loads(data.get("craftsmen"))
            ponds = json.loads(data.get("ponds"))
            data["castles"] = []
            for c in castles:
                data.get("castles").append(cls.CastleResp(**c))
            data["craftsmen"] = []
            for c in craftsmen:
                data.get("craftsmen").append(cls.CraftsMenResp(**c))
            data["ponds"] = []
            for p in ponds:
                data.get("ponds").append(cls.PondResp(**p))
            return data

    name: Optional[str]
    num_of_turns: Optional[int]
    time_per_turn: Optional[int]
    start_time: Optional[datetime]
    id: Optional[int]
    field_id: Optional[int]
    sides: Optional[List[Side]]
    field: Optional[Field]


class GameStatusResp(BaseModel):
    cur_turn: Optional[int]
    max_turn: Optional[int]
    remaining: Optional[int]


class GameActionsStatusResp(BaseModel):
    data: Optional[List[GameActionsResp]]
    status: Optional[GameStatusResp]

