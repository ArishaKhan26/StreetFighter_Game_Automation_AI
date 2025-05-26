# bot.py
from command import Command
from buttons import Buttons
from logger import record      
import joblib
import numpy as np

class Bot:
    # must match the same order as train_model.py button_cols
    BUTTON_ORDER = [
        'A','B','X','Y','L','R','up','down','left','right','start','select'
    ]

    # must match the same order as train_model.py feature_cols
    RESULT_MAP = {'NOT_OVER': 0, 'P1_WIN': 1, 'P2_WIN': 2}

    def __init__(self):
        # Load scaler and model you trained
        self.scaler = joblib.load('scaler.pkl')
        self.model  = joblib.load('bot_model.pkl')

    def extract_features(self, gs):
        """Build features in the exact same order as train_model.py."""
        p1, p2 = gs.player1, gs.player2

        feats = [
            # player1
            p1.player_id,
            p1.health,
            p1.x_coord,
            p1.y_coord,
            int(p1.is_jumping),
            int(p1.is_crouching),
            int(getattr(p1, 'in_move', False)),
            int(getattr(p1, 'move_id', -1)),

            # player2
            p2.player_id,
            p2.health,
            p2.x_coord,
            p2.y_coord,
            int(p2.is_jumping),
            int(p2.is_crouching),
            int(getattr(p2, 'in_move', False)),
            int(getattr(p2, 'move_id', -1)),

            # global
            gs.timer,
            self.RESULT_MAP.get(gs.fight_result, 0),
            int(gs.has_round_started),
            int(gs.is_round_over)
        ]
        return np.array(feats, dtype=float)

    def fight(self, current_game_state, player_slot):
        #Extract & scale
        raw = self.extract_features(current_game_state)
        X_scaled = self.scaler.transform(raw.reshape(1, -1))

        #Predict button presses
        #model.predict returns shape (1, 12) array of 0/1
        pred = self.model.predict(X_scaled)[0]

        #Build Buttons object
        btn = Buttons()
        for i, name in enumerate(self.BUTTON_ORDER):
            setattr(btn, name, bool(pred[i]))

        #Wrap into Command
        cmd = Command()
        if player_slot == "1":
            cmd.player_buttons  = btn
        else:
            cmd.player2_buttons = btn

        #(Optional) log the frame
        #record(current_game_state)

        return cmd
