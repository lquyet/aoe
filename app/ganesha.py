import copy
import random
from itertools import product

from app import helpers
from app.helpers import Side
from app.map import Map
from app.map import create_new_map_from_old_map_and_actions
from app.map_components import AbstractObject, CraftsManA, CraftsManB
from random import randint

from app.models import GameActionsResp


def get_random_action():
    return


def get_random_craftman():
    return


def copy_map_position():
    return


def next_move():
    return


def get_next_possible_states(current_map: Map) -> list[Map]:
    return []


def prediction(current_map: Map, current_turn: int, max_turn: int):
    next_states = get_next_possible_states(current_map)


def get_next_player(current_player: Side) -> Side:
    if current_player == Side.A:
        return Side.B
    return Side.A


def recur_get_states(dic: dict, keys, remain):
    if len(keys) == 1:
        return [[remain.append(dic[keys[0]]) for i in dic[keys[0]]]]

    fn = []
    for k in keys:
        for i in range(len(dic[k])):
            r = recur_get_states(dic, keys[1:], remain.append(dic[k][i]))
            fn += r
    return fn

"""StateNode la 1 trang thai cua ban choi tai 1 thoi diem bat ky"""


class StateNode:
    def __init__(self, current_map: Map, current_turn: int, max_turn: int, recent_action: GameActionsResp):
        self.recent_action = recent_action if recent_action is not None else None
        self.current_map = current_map
        self.current_turn = current_turn
        self.max_turn = max_turn
        self.points = []  # point A, point B
        # children la cac trang thai lien ke cua trang thai hien tai (co the di den voi 1 turn cua 1 ng choi)
        self.children = []

    def clone_with_action(self, list_actions: GameActionsResp):
        new_node = StateNode(create_new_map_from_old_map_and_actions(self.current_map, list_actions), self.current_turn + 1,
                             self.max_turn, list_actions)  # TODO: pull code va dung ham tao cua Thang
        return new_node

    def clone(self):
        return StateNode(copy.deepcopy(self.current_map), self.current_turn, self.max_turn)

    def terminal(self):
        if self.current_turn == self.max_turn:
            return True
        return False

    def get_next_possible_states(self, side: Side):
        if self.current_turn >= self.max_turn:
            return []
        cm_list = []
        ac_list = []
        resp = []
        for craftman in self.current_map._craftsmen:
            if type(craftman) == CraftsManA and side == Side.A:
                cm_list.append(craftman)
            elif type(craftman) == CraftsManB and side == Side.B:
                cm_list.append(craftman)

        for craftman in cm_list:
            stay_action = GameActionsResp.ChildAction(
                action=helpers.ActionType.STAY,
                action_param=None,
                craftsman_id=craftman.craftsmen_id
            )

            build_actions = []
            destroy_actions = []
            for t in helpers.BuildAndDestroyType:
                build_action = GameActionsResp.ChildAction(
                    action=helpers.ActionType.BUILD,
                    action_param=t,
                    craftsman_id=craftman.craftsmen_id
                )
                build_actions.append(build_action)

                destroy_action = GameActionsResp.ChildAction(
                    action=helpers.ActionType.DESTROY,
                    action_param=t,
                    craftsman_id=craftman.craftsmen_id
                )
                destroy_actions.append(destroy_action)

            move_actions = []
            for t in helpers.MoveType:
                move_action = GameActionsResp.ChildAction(
                    action=helpers.ActionType.MOVE,
                    action_param=t,
                    craftsman_id=craftman.craftsmen_id
                )
                move_actions.append(move_action)

            ac_list.append(stay_action + build_actions + destroy_actions + move_actions)

            for items in product(*ac_list):
                res = GameActionsResp(
                    actions = items
                )
                resp.append(self.clone_with_action(res))

        return resp



class GameTree:
    SIMULATION = 1000

    def __init__(self, root: StateNode):
        self.root = root

    def update_current_state(self, root: StateNode):
        self.root = root

    def get_best_next_move(self, state: StateNode, current_player: Side):
        evaluation = {}
        for g in range(self.SIMULATION):
            player = current_player
            stateCopy = state.clone()

            simulation_moves = []
            next_moves = stateCopy.get_next_possible_states()
            score = 1000

            if next_moves != [] and next_moves != None:
                roll = random.randint(len(next_moves) - 1)
                stateCopy = next_moves[roll]

                simulation_moves.append(stateCopy.recent_action)

                if stateCopy.terminal():
                    break

                score -= 1

                current_player = get_next_player(current_player)
                next_moves = stateCopy.get_next_possible_states()

            firstMove = simulation_moves[0]
            lastMove = simulation_moves[-1]






