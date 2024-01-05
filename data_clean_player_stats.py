import pandas as pd
import matplotlib.pyplot as plt
import statistics
from collections import Counter
from playerstats import SortPerformers

#Goal: 
# To delve into player stats to see which players are top performers in various stats categories
#To look into player stats to understand which teams tend to have more top performers in major stats categories

data = pd.read_csv("player_stats_2022_2023.csv")
data.head()

#list of all columns
for col in data.columns:
    print(col)
#list of all teams
teams = set(data["TEAM"])

#DATA CLEANING
data_copy = data

#check for missing data/rows
#No missing values shown using isnull method in any column
data_copy.isnull().sum()

#Remove RANK column
data_copy = data_copy.drop("RANK", axis = 1)
data_copy.head()

#Summary Statistics - whole league
round(data_copy.describe(),2)
#mean number of games played is 42.5

#Removing players who played less than 50% of games
#Since I want to analyze player performance for the whole season, I only want to consider players who played at least half the games.

#Number of players before removing players:
len(data_copy)
#609 players before removing players

#removing players who played less than 41 games:
data_copy = data_copy[data_copy["GP"] >= 41]
len(data_copy)
#327 players left for analysis

#Save cleaned dataset
data_copy.to_csv("cleaned_player_data.csv", index= False)