CREATE DATABASE NBA_player_data;

-- Imported NBA Player stats from 2022-2023
SELECT * FROM player_stats;

-- General Player Stats
-- top 5 oldest nba players based on ranking (include more than 5 if they are tied for age)
SELECT * FROM
(SELECT NAME, AGE, RANK() OVER(ORDER BY AGE DESC) AS ranking FROM player_stats) AS age_rank
WHERE ranking <= 5;

-- top 5 youngest nba players
SELECT * FROM
(SELECT NAME, AGE, RANK() OVER(ORDER BY AGE) AS ranking FROM player_stats) AS age_rank
WHERE ranking <= 5;

-- Oldest player is 42 and youngest is 19 yeard old.



-- Offensive Statistics
-- Find High Point scorers (over 20 PPG) 
SELECT * FROM player_stats
WHERE PPG > 20
ORDER BY PPG DESC;

-- Find players who played over 41 games (50% of games), 
-- score over 20PPG, eFG over 50%, shoot over 50% from 2P, 40% from 3P, and over 60% FT_PERC
SELECT * FROM player_stats
WHERE GP > 41 AND PPG > 20 AND eFG_PERC > 0.5 AND 2P_PERC > 0.5 AND 3P_PERC > 0.4 AND FT_PERC > 0.85
ORDER BY PPG DESC;
-- These players score at a high volume with high efficiency



