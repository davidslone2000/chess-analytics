SELECT 
    played_at,
    focal_player_rating
FROM blitz_games
WHERE played_at >= '2026-03-20'
  AND played_at < '2026-08-21'
ORDER BY played_at ASC;