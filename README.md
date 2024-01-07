# NBA-stat-analysis

# Description

## NBA Player Statistics Analysis 
Includes the analysis of NBA player statistics from the 2022-2023 regular season, which identifies players who are top performers across various combinations of statistical categories. The goal of this analysis was to discover high-performing and well-rounded NBA players based off the available statistics (e.g a player being in the top 10% of players in points, rebounds, and assists per game).

Files: "player_stats_exploration.py", "playerstats.py"

## NBA Team Statistics Analysis
Similarly to the player statistics, NBA team statistics from the 2022-2023 regular season were used to identify teams that were top performers across various combinations of statistical categories to determine whether these teams also had a top rank within the conference the team was in. The goal of this analysis was to identify whether there was a link between performing well at a specific metric and having a strong conference rank, and possible contributing factors towards a top teams success (e.g a team being ranked in the top 3 in their conference also was shown to be a strong offensive team based off metrics).

Files: "team_performance_exploration.py", "playerstats.py"

Additionally, NBA team statistics from the last 5 completed NBA regular seasons (2018-2019 to 2022-2023) were used to identify variables that can be used to create a machine learning model to predict a top 10 regular season record league-wide (not based on conference). 

Files: "team_data_model.py", "team_game_stats_model.py"

## data_clean files
The "data_clean_game_stats.py", "data_clean_player_stats.py", "data_clean_team_data.py" files includes the process of data cleaning and exploratory data analysis to create the final datasets used in the files described in the above subsections.
