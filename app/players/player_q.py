import random
from collections import deque
import tkinter as tk
import tensorflow as tf
import numpy as np

from app.helpers.constants import INIT_WIDTH, INIT_HEIGHT, INFO_BOARD_WIDTH
from app.helpers.enums import ActionType, Side
from app.helpers.utils import new_position_from_direction, DIRECTION_CAN_BUILD_AND_DESTROY, \
    convert_next_action_to_child_action_req
from app.map_controller import MapController
from app.maps.map_q import CustomMapForQ
from app.models import GameResp
from app.objects import AbstractCraftsman, CraftsmanA, CraftsmanB
from app.schemas import NextAction


class PlayerQ(MapController):
    """
        Player với thuật toán Q: Sử dụng Deep Q learning, học tăng cường
        Map:
            - width x height: N x M
            - Numbers of craftsman: C
        State:
            - State của một ô không tính Craftsman: 5
                . WallA, WallB, Pond, Castle, Neutral
            -
            - State của một map không tính Craftsman: 5 x N x M
            - State Craftsman của một map: c(NxM, Cx2) x c(Cx2, C)

        Là một ảnh NxM, có trọng số từ 1 -> 5
        Flat

    """
    _my_map: CustomMapForQ
    q_table_size = []

    def __init__(self, window: tk.Tk, frame: tk.Frame, canvas: tk.Canvas, team_id: int):
        super().__init__(window=window, frame=frame, canvas=canvas, team_id=team_id)
        self.state_size = 636
        self.action_size = 17

        # Khởi tạo replay buffer
        self.replay_buffer = deque(maxlen=50000)

        # Khởi tạo tham số của Agent
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.98
        self.learning_rate = 0.001
        self.update_targetnn_rate = 10

        self.main_network = self.get_nn()
        self.target_network = self.get_nn()

        # Update weight của mạng target = mạng main
        self.target_network.set_weights(self.main_network.get_weights())

    def get_nn(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(32, activation='relu', input_dim=self.state_size))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size))
        model.compile( loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def save_experience(self, state, action, reward, next_state, terminal):
        self.replay_buffer.append((state, action, reward, next_state, terminal))

    def get_batch_from_buffer(self, batch_size):
        exp_batch = random.sample(self.replay_buffer, batch_size)
        state_batch  = np.array([batch[0] for batch in exp_batch]).reshape(batch_size, self.state_size)
        action_batch = np.array([batch[1] for batch in exp_batch])
        reward_batch = [batch[2] for batch in exp_batch]
        next_state_batch = np.array([batch[3] for batch in exp_batch]).reshape(batch_size, self.state_size)
        terminal_batch = [batch[4] for batch in exp_batch]
        return state_batch, action_batch, reward_batch, next_state_batch, terminal_batch

    def train_main_network(self, batch_size):
        state_batch, action_batch, reward_batch, next_state_batch, terminal_batch = self.get_batch_from_buffer(batch_size)

        # Lấy Q value của state hiện tại
        q_values = self.main_network.predict(state_batch, verbose=0)

        # Lấy Max Q values của state S' (State chuyển từ S với action A)
        next_q_values = self.target_network.predict(next_state_batch, verbose=0)
        max_next_q = np.amax(next_q_values, axis=1)

        for i in range(batch_size):
            new_q_values = reward_batch[i] if terminal_batch[i] else reward_batch[i] + self.gamma * max_next_q[i]
            q_values[i][action_batch[i]] = new_q_values

        self.main_network.fit(state_batch, q_values, verbose=0)

    def make_decision(self, state):
        if random.uniform(0,1) < self.epsilon:
            return np.random.randint(self.action_size)
        state = state.reshape((1, self.state_size))
        q_values = self.main_network.predict(state, verbose=0)
        return np.argmax(q_values[0])

    def init_map(self, data: GameResp):
        window_width = INIT_WIDTH
        window_height = INIT_HEIGHT

        if self._frame:
            self._frame.config(width=window_width, height=window_height)
        if self._canvas:
            self._canvas.config(width=window_width - INFO_BOARD_WIDTH, height=window_height)

        self._my_map = CustomMapForQ(canvas=self._canvas,
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

    # def get_next_action_for_craftsman(self, craftsman: AbstractCraftsman) -> NextAction:

