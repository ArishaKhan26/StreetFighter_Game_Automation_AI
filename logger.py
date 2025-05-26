
import csv
import os


LOG_FILE = "training_data.csv"


_csv_file = None
_csv_writer = None

def record(game_state):
    """Append a row of game-state + both players' button states to the CSV."""
    global _csv_file, _csv_writer

    #First time making file
    if _csv_writer is None:
        _csv_file = open(LOG_FILE, mode='a', newline='')
        _csv_writer = csv.writer(_csv_file)

        # If file is brand-new, write header
        if os.path.getsize(LOG_FILE) == 0:
            header = [
                # Player 1
                "player1_id", "player1_health", "player1_x_coord", "player1_y_coord",
                "player1_is_jumping", "player1_is_crouching", "player1_in_move", "player1_move_id",
                "player1_A", "player1_B", "player1_X", "player1_Y",
                "player1_L", "player1_R", "player1_up", "player1_down",
                "player1_left", "player1_right", "player1_start", "player1_select",
                # Player 2
                "player2_id", "player2_health", "player2_x_coord", "player2_y_coord",
                "player2_is_jumping", "player2_is_crouching", "player2_in_move", "player2_move_id",
                "player2_A", "player2_B", "player2_X", "player2_Y",
                "player2_L", "player2_R", "player2_up", "player2_down",
                "player2_left", "player2_right", "player2_start", "player2_select",
                # Global game state
                "timer", "fight_result", "has_round_started", "is_round_over"
            ]
            _csv_writer.writerow(header)
            _csv_file.flush()

    # Extract players
    p1 = game_state.player1
    p2 = game_state.player2

    # Safely handle missing attributes
    p1_in_move = getattr(p1, 'in_move', False)
    p1_move_id = getattr(p1, 'move_id', -1)
    p2_in_move = getattr(p2, 'in_move', False)
    p2_move_id = getattr(p2, 'move_id', -1)

    # Buttons live in `player_buttons`
    pb1 = getattr(p1, 'player_buttons', None)
    pb2 = getattr(p2, 'player_buttons', None)

    # Helper to pull any button safely
    def btn(pb, name):
        return getattr(pb, name, False) if pb is not None else False

    # Build the row
    row = [
        # Player 1 
        p1.player_id, p1.health, p1.x_coord, p1.y_coord,
        p1.is_jumping, p1.is_crouching, p1_in_move, p1_move_id,
        # Player 1 buttons (mix of uppercase & lowercase)
        btn(pb1, 'A'), btn(pb1, 'B'), btn(pb1, 'X'), btn(pb1, 'Y'),
        btn(pb1, 'L'), btn(pb1, 'R'),
        btn(pb1, 'up'), btn(pb1, 'down'),
        btn(pb1, 'left'), btn(pb1, 'right'),
        btn(pb1, 'start'), btn(pb1, 'select'),

        # Player 2
        p2.player_id, p2.health, p2.x_coord, p2.y_coord,
        p2.is_jumping, p2.is_crouching, p2_in_move, p2_move_id,
        # Player 2 buttons
        btn(pb2, 'A'), btn(pb2, 'B'), btn(pb2, 'X'), btn(pb2, 'Y'),
        btn(pb2, 'L'), btn(pb2, 'R'),
        btn(pb2, 'up'), btn(pb2, 'down'),
        btn(pb2, 'left'), btn(pb2, 'right'),
        btn(pb2, 'start'), btn(pb2, 'select'),

        # Global game state
        game_state.timer,
        game_state.fight_result,
        game_state.has_round_started,
        game_state.is_round_over
    ]

    # Write and flush
    _csv_writer.writerow(row)
    _csv_file.flush()
