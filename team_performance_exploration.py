import pandas as pd
from playerstats import SortPerformers, TopPerformers

#Data: Team statistics from the last 5 seasons, includes conference ranking for each season

#Goal: Identify top performers for various statistical categories 


#import cleaned data
data = pd.read_csv('team_stats_2018_2023.csv')
data.head()
data.tail()

#remove Rk column - isn't sorted by conference so its not as meaningful of a stat
#Have the stat in another dataset and also have winning% stat in another dataset
data = data.drop('Rk', axis=1)

#2022-2023 season
#filter for rows with 2022-2023 under 'Year' column
recent_season = data.loc[data['Year'] == '2022-2023']

#DATASETS TO ASSESS TEAM WIN'S AND RANKS (will be used later on):
#win stats (only have 2022-2023 season in this dataset)
data_2 = pd.read_csv('nba_team_stats.csv')

#conference ranking stat
data_3 = pd.read_csv('cleaned_game_stats_fixed_rank.csv')
#filter for 2022-2023 season 
season = data_3.loc[data_3['Year'] == '2022-2023']


#OFFENSIVE METRICS
#finding teams with highest points per game (PTS) 
team_pts = SortPerformers(recent_season, 'PTS')
team_pts.filter_data('Rank_By_Conf', 'Team')

#top 20% of teams in the league(not by conference) for points scored per game
top_pts = team_pts.top_percent(20)
#5/6 these teams are playoff teams. Oklahoma is the exception here, but they likely score more poorly in defensive metrics.

#Let's see if these teams that score the most points per game shoot more 3's as well, since shooting 3's is the most efficient way to get points. 
team_3P = SortPerformers(recent_season, '3P')
top_3P = team_3P.top_percent(20)

#Use TopPerformers class to find the number of teams who are in the top 6 in both PTS and 3P
team_pts_3P = TopPerformers(2, (list(top_pts['Team'])), (list(top_3P['Team'])))
team_pts_3P.top_performers()
#Three out of six teams in the top points per game list are also a top six team in three pointers per game.

#Let's see if they also shoot at a higher 3P percentage.
team_3Pperc = SortPerformers(recent_season, '3P%')
top_3Pperc = team_3Pperc.top_percent(20)

team_pts_3P_3Pperc = TopPerformers(3, list(top_pts['Team']), list(top_3P['Team']), list(top_3Pperc["Team"]))
team_pts_3P_3Pperc.top_performers()
#Both the Golden State Warriors and Boston Celtics are in the top 6 teams in PTS, 3P, and 3P%. 

#Let's also look at the rest of the offensive categories: FG, FG%, 2P and 2P%:
team_FG = SortPerformers(recent_season, "FG")
top_FG = team_FGA.top_percent(20)

team_FGperc = SortPerformers(recent_season, 'FG%')
top_FGperc = team_FGperc.top_percent(20)

team_2P = SortPerformers(recent_season, '2P')
top_2P = team_2P.top_percent(20)

team_2Pperc = SortPerformers(recent_season, '2P%')
top_2Pperc = team_2Pperc.top_percent(20)

#From a quick glance, Boston and Golden State are not a top 6 team in some of these metrics. But maybe some of the other top PTS teams were. 
#Lets see which teams are in the top 6 teams for half the categories, so 4/7 categories!
team_off_metrics = TopPerformers(4, list(top_pts['Team']), list(top_3P['Team']), list(top_3Pperc["Team"]),list(top_FG['Team']), \
list(top_FGperc['Team']),list(top_2P['Team']), list(top_2Pperc['Team']))
team_off_metrics.top_performers()
#Sacremento and Denver are also a top 6 team in 4/7 categories along with Boston and Golden State.

#Let's look at other metrics that contribute to scoring: assists, offensive rebounds, as well as oEFF
#Great passing/teamwork (assists) and having more opportunities to score after misses (offensive rebounds) contribute to offensive performance.

team_ORB = SortPerformers(recent_season, "ORB")
top_ORB = team_ORB.top_percent(20)

team_AST = SortPerformers(recent_season, "AST")
top_AST = team_AST.top_percent(20)

#offensive efficiency (oEFF) - average points the team scored in 100 possessions
team_oEFF = SortPerformers(data_2, 'oEFF')
top_oEFF = team_oEFF.top_percent(20)
#need to remake list to match naming convention of other dataset
new_top_oEFF = ['Cleveland Cavaliers', 'Miami Heat', 'Philadelphia 76ers', 'Toronto Raptors', 'Boston Celtics', 'Phoenix Suns']

#top 20% of teams in league for half of these metrics (5/10)
team_overall_metrics = TopPerformers(5, list(top_pts['Team']), list(top_3P['Team']), list(top_3Pperc["Team"]),list(top_FGA['Team']), \
list(top_FGperc['Team']),list(top_2P['Team']), list(top_2Pperc['Team']), list(top_ORB['Team']), list(top_AST['Team']), new_top_oEFF)
team_overall_metrics.top_performers()
#Four teams here: Sacramento, Golden State, Denver, Boston

#TEAM WIN'S AND RANKS:
#Lets look at the win categories of these four teams:
data_2 = pd.read_csv('nba_team_stats.csv')
data_2.loc[data_2['TEAM'].isin(['Sacramento', 'Golden State', 'Denver', 'Boston'])]
#All of these teams had a winning record (over 0.5 WIN%)!

# Lets find out how they ranked in their respective conferences
data_3 = pd.read_csv('cleaned_game_stats_fixed_rank.csv')
season = data_3.loc[data_3['Year'] == '2022-2023']
season.loc[season['Team'].isin(['Sacramento Kings', 'Golden State Warriors', 'Denver Nuggets', 'Boston Celtics'])]
#Boston, Denver, and Sacramento were all top three teams in their conferences. 
#Golden State is the 6th ranked in the west, which means that they were a playoff team, but likely were not a very high ranking team due to defensive metrics.






#DEFENSIVE METRICS
#opponents PPG (oPPG), defensive rebounds, total rebounds, steals, blocks, defensive efficiency (dEFF)
team_oPPG = SortPerformers(data_2, 'oPPG')
#want it to be ascending, since lower oPPG means teams are scoring less against you
sorted_oPPG = team_oPPG.sorted_stat.sort_values('oPPG')
#top 6 teams:
top_oPPG = sorted_oPPG.iloc[[0,1,2,3,4,5],]
new_top_oPPG = ['Cleveland Cavaliers', 'Miami Heat', 'Philadelphia 76ers', 'Toronto Raptors', 'Boston Celtics', 'Phoenix Suns']

#top dEFF
team_dEFF = SortPerformers(data_2, 'dEFF')
#want it to be ascending, since dEFF represents the amount of points a team allows per 100 possessions by the opposing team
sorted_dEFF = team_oPPG.sorted_stat.sort_values('dEFF')
#top 6 teams:
top_dEFF = sorted_dEFF.iloc[[0,1,2,3,4,5],]
new_top_dEFF = ['Cleveland Cavaliers', 'Memphis Grizzlies', 'Boston Celtics', 'Milwaukee Bucks', 'Chicago Bulls', 'New Orleans Pelicans']
#top teams for both categories
top_def_metrics = TopPerformers(2,list(top_oPPG['TEAM']), list(top_dEFF['TEAM']))
top_def_metrics.top_performers()
#Cleveland and Boston are in the top 6 in the league in top dEFF and top oPPG.

#Lets look at other metrics that likely contribute to defensive performance:
#rebounds
#total rebounds
team_TRB = SortPerformers(recent_season, 'TRB')
top_TRB = team_TRB.top_percent(20) 

#defensive rebounds
team_DRB = SortPerformers(recent_season, 'DRB')
top_DRB = team_DRB.top_percent(20) 

#steals
team_stl = SortPerformers(recent_season, 'STL')
top_stl = team_stl.top_percent(20) 

#blocks
team_blk = SortPerformers(recent_season, 'BLK')
top_blk = team_blk.top_percent(20) 

#Top performers in 3/6 categories
top_def_overall_metrics = TopPerformers(3, new_top_oPPG, new_top_dEFF, list(top_TRB['Team']), list(top_DRB['Team']),\
    list(top_stl['Team']), list(top_blk['Team']))
top_def_overall_metrics.top_performers()
#Interestingly, Cleveland is not a top performers in total or defensive rebounds, or steals or blocks. 
#Memphis, Utah, and Milwaukee seem to perform well with rebounds/steals/blocks.
#This may indicate that those stats don't actually contribute as much to overall defensive performance. 

#Lets look into win and conference ranking stats for Cleveland, Boston, Memphis, and Utah:
#Win stats:
data_2.loc[data_2['TEAM'].isin(['Utah', 'Memphis', 'Cleveland', 'Boston', 'Milwaukee'])]
#Boston, Cleveland and Memphis all had very high win% (over 0.6). Utah is an outlier here with a 0.451 win%. 

# Lets find out how these teams ranked in their respective conferences
season.loc[season['Team'].isin(['Utah Jazz', 'Memphis Grizzlies', 'Cleveland Cavaliers', 'Boston Celtics', 'Milwaukee Bucks'])]
#As expected, Milwaukee, Boston, Cleveland, and Memphis are all ranked very high in their conferences (ranked 1, 2, 4, and 2 respectively).
#Boston also performed well in offensive metrics, scoring in the top 6 in the league in points per game, and other major offensive categories.


#Looking Closer at Utah and Golden State:
#The Golden State Warriors were a top offensive team across many offensive categories yet was ranked 6th in the west.
#The Utah Jazz scored well in several defensive metrics but were ranked 12th in the west. 

#looking closer at "more important" defensive categories
#Comparing defensive performance against top defensive teams.
#oPPG
oPPG = data_2[['TEAM','oPPG']]
oPPG.loc[oPPG['TEAM'].isin(['Utah', 'Memphis', 'Cleveland', 'Boston', 'Milwaukee', 'Golden State'])]

#Golden State and Utah both performed worse in oPPG compared to top ranking teams. 
#Utah may not actually be a strong defensive team despite being a top performer in rebounds and blocks.

#Let's look at dEFF:
dEFF = data_2[['TEAM','dEFF']]
dEFF.loc[dEFF['TEAM'].isin(['Utah', 'Memphis', 'Cleveland', 'Boston', 'Milwaukee', 'Golden State'])]
#Golden State and Utah also did not perform as well in defensive efficiency. 

#Findings:
#Therefore it appears that Golden State was a top offensive team but only finished 6th in the West due to not being a strong defensive team. 
#Utah is not actually a good defensive team when looking closer at their oPPG and dEFF against other teams that scored well in these major defence metrics. 




#TAKEAWAY POINTS:
#Scoring in top 20% of teams (top 6 in league) performance across multiple metrics:
    #Top Offensive Teams: Boston, Golden State, Sacramento, Denver
    #Top Defensive Teams: Memphis, Cleveland, Boston, Milwaukee

#Boston appeared to have been a top team due to being both a strong offensive AND defensive team.
#Milwaukee was ranked first in the east, Cleveland fourth in the east, and Memphis second in the West, and this is due to being good defensive teams. 
#Golden State was very strong on offense but not defence, which is why they were ranked only 6th in the West.
#Utah is strong rebounding and blocks but not on defense overall. 





