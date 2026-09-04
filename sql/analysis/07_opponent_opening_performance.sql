SELECT 
    COUNT(*) AS games,
    opening_family,
    focal_player_color,
    ROUND(
    COUNT(*) FILTER(WHERE focal_player_result = 'win') / 
    COUNT(*)::DECIMAL * 100, 2)  AS win_percentage,
    ROUND(
    COUNT(*) FILTER(WHERE focal_player_result = 'loss') / 
    COUNT(*)::DECIMAL * 100, 2)  AS loss_percentage,
    ROUND(
    COUNT(*) FILTER(WHERE focal_player_result = 'draw') / 
    COUNT(*)::DECIMAL * 100, 2) AS draw_percentage
FROM blitz_games

JOIN openings ON
    blitz_games.opening_url = openings.opening_url

WHERE played_at >= '2026-03-20'
  AND played_at < '2026-08-21'
  AND (
        (opening_family = 'Scandinavian Defense' AND focal_player_color = 'white')
    OR (opening_family = 'Philidor Defense' AND focal_player_color = 'white')
    OR (opening_family = 'French Defense' AND focal_player_color = 'white')
    OR (opening_family = 'Caro Kann Defense' AND focal_player_color = 'white')
    OR (opening_family = 'Queens Pawn Opening' AND focal_player_color = 'black')
    OR (opening_family = 'Sicilian Defense' AND focal_player_color = 'white')
   )
GROUP BY opening_family, focal_player_color
ORDER BY games DESC;