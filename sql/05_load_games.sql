-- Transform raw Chess.com monthly archive data and load it
-- into the analysis-ready games table.

-- The games table is fully derived from raw_archives, so it is
-- truncated and rebuilt each time this script runs.

TRUNCATE TABLE games;

INSERT INTO games (
    game_id,
    played_at,
    time_class,
    time_control,
    rated,
    game_url,
    opening_url,
    eco_code,
    move_count,
    focal_player_color,
    focal_player_rating,
    opponent_username,
    opponent_rating,
    focal_player_raw_result,
    focal_player_result,
    termination_type,
    focal_player_first_move,
    opponent_first_move
)

SELECT
    (game ->> 'uuid')::UUID AS game_id,

    TO_TIMESTAMP(
        (game ->> 'end_time')::BIGINT
    ) AS played_at,

    game ->> 'time_class' AS time_class,

    game ->> 'time_control' AS time_control,

    (game ->> 'rated')::BOOLEAN AS rated,

    game ->> 'url' AS game_url,

    game ->> 'eco' AS opening_url,

    substring(
        game ->> 'pgn'
        FROM '\[ECO "([^"]+)"\]'
    ) AS eco_code,

    (
        split_part(
            game ->> 'fen',
            ' ',
            6
        )
    )::INTEGER AS move_count,
    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
            THEN 'white'
        ELSE 'black'
    END AS focal_player_color,

    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
            THEN (game -> 'white' ->> 'rating')::INTEGER
        ELSE (game -> 'black' ->> 'rating')::INTEGER
    END AS focal_player_rating,

    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
            THEN game -> 'black' ->> 'username'
        ELSE game -> 'white' ->> 'username'
    END AS opponent_username,

    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
            THEN (game -> 'black' ->> 'rating')::INTEGER
        ELSE (game -> 'white' ->> 'rating')::INTEGER
    END AS opponent_rating,

    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
            THEN game -> 'white' ->> 'result'
        ELSE game -> 'black' ->> 'result'
    END AS focal_player_raw_result,

    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
             AND game -> 'white' ->> 'result' = 'win'
            THEN 'win'

        WHEN game -> 'black' ->> 'username' = 'davidslone2000'
             AND game -> 'black' ->> 'result' = 'win'
            THEN 'win'

        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
             AND game -> 'black' ->> 'result' = 'win'
            THEN 'loss'

        WHEN game -> 'black' ->> 'username' = 'davidslone2000'
             AND game -> 'white' ->> 'result' = 'win'
            THEN 'loss'

        ELSE 'draw'
    END AS focal_player_result,
    CASE
        WHEN game -> 'white' ->> 'result' = 'win'
            THEN game -> 'black' ->> 'result'
        ELSE game -> 'white' ->> 'result'
    END AS termination_type,

    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
            THEN (
                regexp_match(
                    split_part(game ->> 'pgn', E'\n\n', 2),
                    '^1\. ([^ ]+)'
                )
            )[1]
        ELSE (
            regexp_match(
                split_part(game ->> 'pgn', E'\n\n', 2),
                '1\.\.\. ([^ ]+)'
            )
        )[1]
    END AS focal_player_first_move,

    CASE
        WHEN game -> 'white' ->> 'username' = 'davidslone2000'
            THEN (
                regexp_match(
                    split_part(game ->> 'pgn', E'\n\n', 2),
                    '1\.\.\. ([^ ]+)'
                )
            )[1]
        ELSE (
            regexp_match(
                split_part(game ->> 'pgn', E'\n\n', 2),
                '^1\. ([^ ]+)'
            )
        )[1]
    END AS opponent_first_move

FROM raw_archives,
     jsonb_array_elements(raw_json -> 'games') AS game;

-- Verify that all games were loaded.

SELECT COUNT(*) AS loaded_game_count
FROM games;
