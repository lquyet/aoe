from itertools import product

from mctspy.games.common import AbstractGameAction, TwoPlayersAbstractGameState

from app import utils, helpers
from app.helpers import Side
from app.map import Map, create_new_map_from_old_map_and_actions
from app.map_components import CraftsManA, CraftsManB
from app.models import GameActionsResp


# A move is a list of N actions where N is the number of craftsmen
# In the other words, a move represents a turn each player takes
class ProconGameMove(AbstractGameAction):
    def __init__(self, actions: GameActionsResp):
        self.actions = actions


class ProconGameState(TwoPlayersAbstractGameState):
    def __init__(self, current_map: Map, current_turn: int, max_turn: int, recent_action: GameActionsResp, next_to_move: Side):
        self.recent_action = recent_action if recent_action is not None else None
        self.current_map = current_map
        self.current_turn = current_turn
        self.next_to_move = next_to_move
        self.max_turn = max_turn
        self.points = []  # point A, point B
        # children la cac trang thai lien ke cua trang thai hien tai (co the di den voi 1 turn cua 1 ng choi)
        self.children = []
        self.parent = None

    def game_result(self):
        """
        this property should return:

         1 if player #1 wins
        -1 if player #2 wins
         0 if there is a draw
         None if result is unknown

        Returns
        -------
        int

        """
        self.points = self.current_map.calculate_point()
        if self.points[0] > self.points[1]:
            # player A win
            return 1
        elif self.points[0] < self.points[1]:
            # player B win
            return -1
        else:
            # draw
            return 0

    def is_game_over(self):
        """
        boolean indicating if the game is over,
        the simplest implementation may just be
        `return self.game_result() is not None`

        Returns
        -------
        boolean

        """
        return self.current_turn > self.max_turn

    def move(self, actions: GameActionsResp):
        """
        consumes action and returns resulting TwoPlayersAbstractGameState

        Parameters
        ----------
        actions: AbstractGameAction, in this case is GameActionResp which stores a list of actions for all craftsmen

        Returns
        -------
        TwoPlayersAbstractGameState

        """
        return ProconGameState(create_new_map_from_old_map_and_actions(self.current_map, actions),
                               self.current_turn + 1,
                               self.max_turn, actions, utils.get_next_move(self.next_to_move))

    def get_legal_actions(self):
        """
        returns list of legal action at current game state
        Returns
        -------
        list of AbstractGameAction

        """
        if self.current_turn > self.max_turn:
            return []

        cm_list = []
        ac_list = []
        gameActionResp = []

        for craftsman in self.current_map._craftsmen:
            if type(craftsman) == CraftsManA and self.next_to_move == Side.A:
                cm_list.append(craftsman)
            elif type(craftsman) == CraftsManB and self.next_to_move == Side.B:
                cm_list.append(craftsman)

        for craftsman in cm_list:
            stay_actions = []
            stay_action = GameActionsResp.ChildAction(
                action=helpers.ActionType.STAY,
                action_param=None,
                craftsman_id=craftsman.craftsmen_id
            )
            stay_actions.append(stay_action)

            build_actions = []
            destroy_actions = []
            for t in helpers.BuildAndDestroyType:
                build_action = GameActionsResp.ChildAction(
                    action=helpers.ActionType.BUILD,
                    action_param=t,
                    craftsman_id=craftsman.craftsmen_id
                )
                build_actions.append(build_action)

                destroy_action = GameActionsResp.ChildAction(
                    action=helpers.ActionType.DESTROY,
                    action_param=t,
                    craftsman_id=craftsman.craftsmen_id
                )
                destroy_actions.append(destroy_action)

            move_actions = []
            for t in helpers.MoveType:
                move_action = GameActionsResp.ChildAction(
                    action=helpers.ActionType.MOVE,
                    action_param=t,
                    craftsman_id=craftsman.craftsmen_id
                )
                move_actions.append(move_action)

            ac_list.append(stay_actions + build_actions + destroy_actions + move_actions)

        for action_combination in product(*ac_list):
            gameActionResp.append(GameActionsResp(actions=action_combination))

        return gameActionResp
