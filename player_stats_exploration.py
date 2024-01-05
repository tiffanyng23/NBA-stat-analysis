import pandas as pd
import matplotlib.pyplot as plt
import statistics
import numpy as np
from collections import Counter
from playerstats import SortPerformers, TopPerformers
import scipy


#PLAYER ANALYSIS USING 2022-2023 SEASON DATA:

#Goals
#To delve into player stats to see which players are top performers in various stats categories
#Combine top perfomer results across various related stat categories to determine players who are top performers across multiple stat categories
#This indicates how well-rounded the player is (e.g being a top performer in PPG, RPG, and APG)

#DATA
# Data has been cleaned in another module - steps shown in "NBA_player_data_cleaning.py"
# Includes players who played at least 50% of games to ensure player stats are shown consistently throughout the season.
data_copy = pd.read_csv("cleaned_player_data.csv")
data_copy.head()

#list of all columns
data_copy.columns

#Summary Statistics
round(data_copy.describe(), 2)


#Histograms
#Creating histograms to visualize the distribution of various statistical categories
var_hist = ["AGE", "MPG", "PPG", "RPG", "APG", "SPG", "BPG", "FTA", "FT%", "2PA", "2P%", "3PA", "3P%", "TPG", "ORtg", "DRtg"]

ncols = 4
nrows = int(np.ceil(len(var_hist)/ncols))
fig, ax = plt.subplots(nrows = nrows, ncols = ncols)

for i, var in enumerate(var_hist):
    row = int(np.floor(i/ncols))
    col = i % ncols
    ax[row,col].hist(data_copy[var], color = "pink", density = True)
    ax[row,col].set_title(var)
plt.tight_layout()
plt.show()

#Evidently many of the statistical categories are positively skewed, with a few players performing at a higher level.


#Explanation of Skew:
    
#Measuring skewness:
skewness_results = {}
for var in var_hist:
    skew_var = round(scipy.stats.skew(data_copy[var], axis = 0),2)
    skewness_results[f"{var}"] = skew_var

#print stats that have a positive skew over 1 and negative skew below -1
for var, skewness in skewness_results.items():
    if (skewness > 1) or (skewness < -1):
        print(f"{var}: {skewness}")
        

#The stat categories that have these skews tend to volume-based so they depend on playing time/responsibilities.
#There are only so many minutes in a game, so there is a limited amount of opportunities for shot attempts, rebounds, or assists, for example. 
#Players with more playing time and responsibility would have more opportunities to have high numbers in volume-based stats.
#Statistical categories that are not volume-based such as shooting percentage or offensive/defensive rating, tend to be normally distributed.

#No observations will be removed since the values occured solely due to player performance.
#I will be focusing on exploring the data to find top performers in various stat categories. 


#TOP 10% PERFORMERS in PPG + RPG + APG
#Use SortPerformers class from the playerstats module

#PPG
#Sort and filter for PPG
player_ppg = SortPerformers(data_copy, "PPG")
print(player_ppg)
#sorted by PPG in descending order
player_ppg.sorted_stat
#filter for name, team, and stat of interest for better readability
filtered_data = player_ppg.filter_data("NAME", "TEAM")
#getting top ppg performers 
top_ppg = player_ppg.top_percent(10)

#RPG
player_rpg = SortPerformers(data_copy, "RPG")
player_rpg.sorted_stat
#filters out columns for better readability
filtered_rpg = player_rpg.filter_data("NAME", "TEAM")
#top rpg performers
top_rpg = player_rpg.top_percent(10)

#APG
player_apg = SortPerformers(data_copy, "APG")
filtered_apg = player_apg.filter_data("NAME", "TEAM")
#top apg performers
top_apg = player_apg.top_percent(10)


#Players in the top 10% for points, rebounds, and assists per game:

#Steps:
# I created a class called TopPerformers which is in the playerstats module 
# The function will combine lists of players for a chosen number of stat categories to create one list of top performers
# Then it will count the number of times a player is on this list

#convert top_performer results to a single list 
total = TopPerformers(3, list(top_apg["NAME"]), list(top_rpg["NAME"]), list(top_ppg["NAME"]))
total.top_performers()

#Interpretation of Results:
#4 players are in the top 10% for PPG, RPG, and APG: 'Giannis Antetokounmpo', 'Nikola Jokic', 'LeBron James', 'Luka Doncic'
#this stat is different than the P+R+A stat, since having a high total in one of the categories (especially points), could skew the results
#This accounts for that and shows players that are top performers in these 3 categories, indicating well-rounded abilities



#TOP 10% PERFORMERS: SHOOTING% STATS
#Including: FT%, 2P%, 3P%, eFG%, TS%

#How to account for players with low shot attempts:
# Low shot attempts often skews results. This is partially accounted for when I filtered out players who played less than 50% of games.
# Filtering out by games played doesn't account for players who don't attempt many 3P shots.

#Solution: Will only include players in the 25th percentile or higher for shot attempts (FT, 2P, and 3P):
data_copy[["2PA", "3PA", "FTA"]].describe()

#Free Throws
#FT attempts
ft_attempts = SortPerformers(data_copy, "FTA")
ft_attempts.sorted_stat
#filter for top 75% of players
filtered_fta = ft_attempts.top_percent(75)
#Top FT% - using dataset that filtered for the top 25th percentile or higher for FTA
ft_perc = SortPerformers(filtered_fta, "FT%")
ft_perc.sorted_stat
#top 10% of FT%
top_ft_perc = ft_perc.top_percent(10)

#Two pointers
#2PA
twopa = SortPerformers(data_copy, "2PA")
#top 75% of players
filtered_twopa = twopa.top_percent(75)
#Top 2P% - using filtered 2PA data
two_perc = SortPerformers(filtered_twopa, "2P%")
#top 10% of FT%
top_2P_perc = two_perc.top_percent(10)

#Three Pointers
three_pa = SortPerformers(data_copy, "3PA")
filtered_3PA = three_pa.top_percent(75)
#Top 3P%
three_perc = SortPerformers(filtered_3PA, "3P%")
top_3P_perc = three_perc.top_percent(10)
#filter for just name , 3PA, and 3P%
three_perc.filter_data("NAME", "3PA")


#Creating new FGA category:
#Made a new field goal attempt category to only include FG% ranking for those who are in the top 75% of FGA
# Done by adding 2PA and 3PA together for each player

#List of total 2PA and 3PA:
list_2pa = list(data_copy["2PA"])
list_3pa = list(data_copy["3PA"])

#Creating total FGA list 
fga = []
for a, b in zip(list_2pa, list_3pa):
    total_attempts = a+b
    fga.append(total_attempts)

#Creating new FGA column in dataset
data_copy["FGA"] = fga

#top 75% of players for FGA
total_fga = SortPerformers(data_copy, "FGA")
filtered_fga = total_fga.top_percent(75)
#Yse filtered FGA dataset for top eFG% and TS% - this ensures that players with low attempts are not included

#Top eFG%
efg_perc = SortPerformers(filtered_fga, "eFG%")
efg_perc.sorted_stat
top_efg = efg_perc.top_percent(10)

#Top TS%
ts_perc = SortPerformers(filtered_fga, "TS%")
top_ts_perc = ts_perc.top_percent(10)
ts_perc.filter_data("NAME")


#Players in top 10% of all shooting% statistics
#filter for names in each shooting* category
total_shot_perc = TopPerformers(3, list(top_ft_perc["NAME"]), list(top_2P_perc["NAME"]), list(top_3P_perc["NAME"]),\
    list(top_efg["NAME"]), list(top_ts_perc["NAME"]))

#Lets try 3 (none for 4/5 or 5/5):
total_shot_perc.top_performers()
#17 players on list
len(total_shot_perc.top_performers())

#Interpretation of Results:
# 17 players: {'Walker Kessler', 'Rudy Gobert', 'Onyeka Okongwu', 'Nic Claxton', 'Domantas Sabonis', 
# 'Daniel Gafford', 'Larry Nance Jr.', 'Nikola Jokic', 'Mason Plumlee', 'Clint Capela', 'Jarrett Allen', 
# 'Jalen Duren', 'Brandon Clarke', 'Thomas Bryant', 'Corey Kispert', 'Drew Eubanks', 'Stephen Curry'}
#This statistic includes all shooting % categories, but doesn't account for the ratio at which the players shoot close to the basket compared to three pointers
#Therefore it would bias for players who mostly score near the basket (especially since it included the top 10% for only 3/5 of the categories!) 
#Therefore this statistic would be a better indicator of scoring efficiency than shooting ability, which is also very important!


#Top 10% statistic for FT% + 2P% + 3P% statistic: 
# This would better show overall shooting ability
top_shooting_perc = TopPerformers(2, list(top_ft_perc["NAME"]), list(top_2P_perc["NAME"]), list(top_3P_perc["NAME"]))
#No player is in the top 10% for all 3 categories
#2/3 categories:
top_shooting_perc.top_performers()
#Interpretation of Results:
#4 players: {'Bojan Bogdanovic', 'Damion Lee', 'Klay Thompson', 'Stephen Curry'}
#These 4 players are known to be very strong shooters and are in the top 10% for 2/3 of FT%, 2P%, and 3P%


#Can also see who the top 3P% shooters are while also being a high volume shooter:
#Top 10% of players in 3P attempts:
three_pa = SortPerformers(data_copy, "3PA")
top_3PA = three_pa.top_percent(10)

#extracting players
full_threes = TopPerformers(2, list(top_3PA["NAME"]), list(top_3P_perc["NAME"]))
full_threes.top_performers()
#Interpretation of Results:
#5 players are in the top 10% in both 3PA and 3P%: {'Michael Porter Jr.', 'Buddy Hield', 'Klay Thompson', 'Keegan Murray', 'Stephen Curry'}
#This statistic indicates that these players are likely the highest impact 3P shooters in the 2022-2023 season!
#These players shoot a high volume of three's at a high shooting percentage.
#This statistic removes players who have a high shooting percentage but below league median in attempts.

#Stephen Curry:
# In the top 10% in 3PA+3P%, top 10% of 3/5 of (FT%, 2P%, 3P%, eFG%, TS%), and top 10% of 2/3 of (FT%, 2P% and 3P%). 
# He is often regarded as the best shooter in the NBA, and this is evidence as he has top statistics for many shooting categories.


#Top 2P% while being a high volume 2P scorer:
#top 10% of players for 2PA
twopa = SortPerformers(data_copy, "2PA")
top_2PA = twopa.top_percent(10)

#extracting players
full_twos = TopPerformers(2,list(top_2PA["NAME"]), list(top_2P_perc["NAME"]))
full_twos.top_performers()
#Interpretation of Results:
#Two players are in the top 10% in both 2PA and 2P%: {'Nikola Jokic', 'Domantas Sabonis'}
#This statistic biases for players who score heavily in the paint, though both Nikola and Domantas shoot some 3's as well.
#This shows that they are likely both great all-around offensive players! 

#Nikola Jokic stats
top_2PA.loc[top_2PA["NAME"] == "Nikola Jokic"]
#Domantas Sabonis stats
top_2PA.loc[top_2PA["NAME"] == "Domantas Sabonis"]


#Top FT% for those who shot high amount of free throws:
#top 10% of players for FT attempts:
fta = SortPerformers(data_copy, "FTA")
top_fta = fta.top_percent(10)

full_ft = TopPerformers(2, list(top_fta["NAME"]), list(top_ft_perc["NAME"]))
full_ft.top_performers()
#Interpretation of Results:
#3 players: {'Trae Young', 'Damian Lillard', 'Shai Gilgeous-Alexander'} 
#These players score a lot of points through free throws since they shoot it at a high % and have high attempts

#FINAL POINTS:
#This was intended to identify top performers across different combinations of offensive categories.
#I focused on players who do well on shooting percentages while doing so throughout the season and with a high volume of shot attempts. 
#This was done with the goal of identifying top all-around offensive performers. 
#Players such as Stephen Curry, Nikola Jokic, Klay Thompson, Domantas Sabonis appear to be top 10% performers across several combinations of categories. 
#This is a strong indication that they are strong offensive players. 
#Curry and Thompson are known to be very strong shooters while Sabonis and Jokic are known to be strong scorers around the paint. 























