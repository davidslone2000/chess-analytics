WITH ordered_games AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            ORDER BY played_at ASC
        ) AS game_order_asc,

        ROW_NUMBER() OVER (
            ORDER BY played_at DESC
        ) AS game_order_desc

    FROM blitz_games
    WHERE played_at >= '2026-03-20'
    AND played_at < '2026-08-21'
)

SELECT 
    COUNT(*) AS total_games,
    COUNT(*) FILTER(WHERE focal_player_result = 'win') AS wins,
    COUNT(*) FILTER(WHERE focal_player_result = 'loss') AS losses,
    COUNT(*) FILTER(WHERE focal_player_result = 'draw') AS draws,
    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'win') /
        COUNT(*)::DECIMAL *100, 2
    ) AS win_percentage,
    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'loss') /
        COUNT(*)::DECIMAL *100, 2
    ) AS loss_percentage,
    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'draw') /
        COUNT(*)::DECIMAL *100, 2
    ) AS draw_percentage, 
    MAX(focal_player_rating) FILTER (
        WHERE game_order_asc = 1
    ) AS starting_rating,
    MAX(focal_player_rating) FILTER (
        WHERE game_order_desc = 1
    ) AS current_rating, 

    MAX(focal_player_rating) FILTER (
        WHERE game_order_desc   = 1
    )
    -
    MAX(focal_player_rating) FILTER (
        WHERE game_order_asc = 1
    ) AS rating_change

FROM ordered_games;
