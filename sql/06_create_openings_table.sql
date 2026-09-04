-- Create a table to store chess.com opening information, 
--and populate it with unique openings from the blitz_games table. 

-- This allowed for investigation into opening analytics 
--by joining the openings table to the blitz_games table on opening_url.

CREATE TABLE openings (
    opening_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    opening_url TEXT UNIQUE NOT NULL,
    eco_code TEXT NOT NULL,
    opening_name TEXT NOT NULL,
    opening_family TEXT
);

INSERT INTO openings (
    opening_url,
    eco_code,
    opening_name,
    opening_family
)

SELECT DISTINCT
    opening_url,
    eco_code,
    REPLACE(
            REPLACE(opening_url, 'https://www.chess.com/openings/', ''), 
            '-',' ') AS opening_name,
    substring(
        REPLACE(
            REPLACE(opening_url, 'https://www.chess.com/openings/', ''), 
            '-', 
            ' ')
    FROM '^(.+?(Defense|Opening|Game|Attack|Gambit|System))'
    ) AS opening_family
FROM blitz_games
WHERE opening_url IS NOT NULL;