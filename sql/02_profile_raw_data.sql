-- Expand the monthly Chess.com "games" JSON array into one row per game
-- and extract the game URL as text.

SELECT
    source_month,
    game ->> 'url' AS game_url
FROM raw_archives,
     jsonb_array_elements(raw_json -> 'games') AS game
WHERE source_month = '2026-08-01';

-- Identify all White/Black result combinations present in the raw data.
-- Used to determine how Chess.com represents wins, losses, and draws.

SELECT DISTINCT
    game -> 'white' ->> 'result' AS white_result,
    game -> 'black' ->> 'result' AS black_result
FROM raw_archives,
     jsonb_array_elements(raw_json -> 'games') AS game
ORDER BY white_result, black_result;

SELECT
    COUNT(*) AS total_games,
    COUNT(DISTINCT game ->> 'uuid') AS unique_game_ids
FROM raw_archives,
     jsonb_array_elements(raw_json -> 'games') AS game;
