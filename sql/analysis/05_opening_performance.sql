SELECT
    COUNT(*) AS games_played,
    focal_player_color,
    opening_family, 
    ROUND(
        COUNT(*) FILTER (WHERE focal_player_result = 'win') /
        COUNT(*)::DECIMAL * 100, 2
    ) AS win_percentage,
    ROUND(
        COUNT(*) FILTER (WHERE focal_player_result = 'loss') /
        COUNT(*)::DECIMAL * 100, 2
    ) AS loss_percentage, 
    ROUND(
        COUNT(*) FILTER (WHERE focal_player_result = 'draw') /
        COUNT(*)::DECIMAL * 100, 2
    ) AS draw_percentage

FROM blitz_games

JOIN openings 
    ON blitz_games.opening_url = openings.opening_url

WHERE played_at >= '2026-03-20'
  AND played_at < '2026-08-21'
  AND (
       (opening_family = 'Scandinavian Defense' AND focal_player_color = 'black')
    OR (opening_family = 'Dutch Defense' AND focal_player_color = 'black')
    OR (opening_family = 'Indian Game' AND focal_player_color = 'black')
    OR (opening_family = 'Italian Game' AND focal_player_color = 'white')
    OR (opening_family = 'Giuoco Piano Game' AND focal_player_color = 'white')
    OR (opening_family = 'Scotch Game' AND focal_player_color = 'white')
  )

GROUP BY focal_player_color, opening_family

ORDER BY COUNT(*) DESC;