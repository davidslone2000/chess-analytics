SELECT
    termination_type,
    COUNT(*) FILTER (WHERE focal_player_result = 'win') AS won_by_count,
    COUNT(*) FILTER (WHERE focal_player_result = 'loss') AS lost_by_count
FROM blitz_games
WHERE played_at >= '2026-03-20'
  AND played_at < '2026-08-21'
  AND focal_player_result IN ('win', 'loss')
GROUP BY termination_type;