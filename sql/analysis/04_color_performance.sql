SELECT
    focal_player_color,
    COUNT(*) AS total_games,

    ROUND(
        COUNT(*) FILTER (
            WHERE focal_player_result = 'win'
        )::DECIMAL
        / COUNT(*) * 100,
        2
    ) AS win_percentage,

    ROUND(
        COUNT(*) FILTER (
            WHERE focal_player_result = 'loss'
        )::DECIMAL
        / COUNT(*) * 100,
        2
    ) AS loss_percentage,

    ROUND(
        COUNT(*) FILTER (
            WHERE focal_player_result = 'draw'
        )::DECIMAL
        / COUNT(*) * 100,
        2
    ) AS draw_percentage

FROM blitz_games
WHERE played_at >= '2026-03-20'
  AND played_at < '2026-08-21'

GROUP BY focal_player_color
ORDER BY focal_player_color;