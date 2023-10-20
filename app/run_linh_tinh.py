from app.players.player_q import PlayerQ
import numpy as np

player_q = PlayerQ(window=None, frame=None, canvas=None, team_id=None)

player_q.make_decision(state=np.array([1, 2, 3, 4, 5]))
