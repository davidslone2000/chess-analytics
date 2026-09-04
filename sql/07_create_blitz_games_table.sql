--only interest in blitz games for this project, so create a blitz_games table to store only 
--those games

CREATE VIEW blitz_games AS(
    SELECT *
    FROM games
    WHERE time_class = 'blitz'
);