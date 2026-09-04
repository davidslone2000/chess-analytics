-- Create a clean table to store the transformed chess.com game data.

CREATE TABLE games (
    game_id UUID PRIMARY KEY,
    played_at TIMESTAMPTZ,
    time_class TEXT,
    time_control TEXT,
    rated BOOLEAN,
    game_url TEXT,
    opening_url TEXT,
    eco_code TEXT,
    move_count INTEGER,
    focal_player_color TEXT,
    focal_player_rating INTEGER,
    opponent_username TEXT,
    opponent_rating INTEGER,
    focal_player_raw_result TEXT,
    focal_player_result TEXT,
    termination_type TEXT,
    focal_player_first_move TEXT,
    opponent_first_move TEXT
);
