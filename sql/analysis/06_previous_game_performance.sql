WITH blitz_w_previous AS (
    SELECT
        *,
        LAG(focal_player_result) OVER (
            ORDER BY played_at
        ) AS previous_result,

        LAG(played_at) OVER (
            ORDER BY played_at
        ) AS previous_played_at

    FROM blitz_games
    WHERE played_at >= '2026-03-20'
        AND played_at < '2026-08-21'
)

SELECT 
    COUNT(*) FILTER (WHERE previous_result = 'win') AS games_after_wins,
    COUNT(*) FILTER (WHERE previous_result = 'loss') AS games_after_losses,
    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'win' AND previous_result = 'win') / 
        (COUNT(*) FILTER(WHERE previous_result = 'win'))::DECIMAL * 100, 2)  AS win_percent_after_wins, 
    
    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'loss' AND previous_result = 'win') / 
        (COUNT(*) FILTER(WHERE previous_result = 'win'))::DECIMAL * 100, 2)  AS loss_percent_after_wins,
    
    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'draw' AND previous_result = 'win') / 
        (COUNT(*) FILTER(WHERE previous_result = 'win'))::DECIMAL * 100, 2)  AS draw_percent_after_wins,

    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'win' AND previous_result = 'loss') / 
        (COUNT(*) FILTER(WHERE previous_result = 'loss'))::DECIMAL * 100, 2)  AS win_percent_after_loss,

    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'loss' AND previous_result = 'loss') / 
        (COUNT(*) FILTER(WHERE previous_result = 'loss'))::DECIMAL * 100, 2)  AS loss_percent_after_loss,

    ROUND(
        COUNT(*) FILTER(WHERE focal_player_result = 'draw' AND previous_result = 'loss') / 
        (COUNT(*) FILTER(WHERE previous_result = 'loss'))::DECIMAL * 100, 2)  AS draw_percent_after_loss
FROM blitz_w_previous
WHERE played_at - previous_played_at <= INTERVAL '10 minutes';