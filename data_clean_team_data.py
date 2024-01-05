import pandas as pd
import matplotlib.pyplot as plt
import statistics
from playerstats import SortPerformers
import numpy as np
from scipy.stats import norm

#DATASET
#NBA team statistics for 2022-2023 seasons
data = pd.read_csv("nba_team_stats.csv")
data.head()

#column names
for col in data.columns:
    print(col)

#DATA CLEANING
data_copy = data

#check for missing data/rows
data_copy.isnull().sum()
# Missing values seen in Rank column
# Will fix this!

#Columns to remove due to complexity/not relevant: 
# winning/losing streak (STRK) - this is a transient stat, not relevant since it only shows the most recent streak
# rSOS (remaining strength of schedule) - season is done so not relevant
#Winning stats: I will be predicting ranking/wins so no need to have extra stats to represent wins
# ACH (actual vs expected winning percentage)
# pWIN% (projected win%)
# eWIN% (ideal winning percentage)

data_copy = data_copy.drop(["STRK", "ACH", "pWIN%", "eWIN%", "rSOS"], axis=1)

#FIX RANK COLUMN
# Replace NaN with correct values (1 to 30)
new_rank = [num for num in range(1,31)]
#sort data by win%
sort_wins = SortPerformers(data_copy, "WIN%")
sort_wins_data = sort_wins.sorted_stat

#Create new ranking column
# use rank method to account for equal win%, use method = min argument for ranking ties
rank = sort_wins_data["WIN%"].rank(method = "min", ascending= False)
#creating ranking list
ranking = []
for n in rank:
    ranking.append(int(n))
#New ranking column
sort_wins_data["RANKING"] = ranking

#Delete previous rank column
clean_data = sort_wins_data.drop("RANK", axis=1)
#confirming that old rank column was dropped and ties in win% is handled by ranking by min value
clean_data.head(6)

#FIX INDEXING
# reset old index to form a new one
clean_data = clean_data.reset_index()
#delete original index column (out of order due to changing the way the data is sorted)
clean_data = clean_data.drop("index", axis =1)

#data to be used for analysis
#confirming ranking is from 1 to 30
clean_data.head()
clean_data.tail()


#EXPLORATORY DATA ANALYSIS
#Sumary Statistics
round(clean_data.describe(),2)
#mean and median values appear to be similar across all variables
#The data is not likely to have a lot of outliers since means and medians are similar, but will confirm with boxplots

#Boxplots:
#Visualize outliers and percentile statistics
boxplot_data = ["PPG", "oPPG", "pDIFF", "PACE", "dEFF", "eDIFF", "oEFF","WIN%", "SOS", "CONS", "A4F", "SAR"]

ncol_bp = 4
nrow_bp = int(np.ceil(len(boxplot_data)/ncol_bp))

fig,axes = plt.subplots(nrow_bp, ncol_bp, figsize= (15,15))
for i, var in enumerate(boxplot_data):
    row = int(np.floor(i/ncol_bp))
    col = i % ncol_bp

    axes[row,col].boxplot(clean_data[var], patch_artist=True,
            boxprops=dict(facecolor="blue", color="green", linewidth=2),
            whiskerprops=dict(color="black", linewidth=2), 
            medianprops=dict(color="black", linewidth=1), 
            capprops=dict(color="black", linewidth=2),
            flierprops=dict(markerfacecolor="purple", marker="o", markersize=7))
    axes[row,col].set_title(var)

plt.tight_layout()
plt.show()

# There are a few outliers in the data.
# This includes point difference (pDIFF), eDIFF, offensive efficiency (oEFF), win percentage (win%), A4F, and SAR.
# These outliers should not be an issues since they occured naturally (its dependent on how the team performs at the specified metric)
# Will calculate z-scores for each point. If the standard deviation of any value is over 3 (absolute value), then I will remove it.

#Calculating z score for all the points for variables in the boxplots.
#Formula: z = (x-mu)/sigma

for var in boxplot_data:
    #rename variable data to data
    data = clean_data[var]
    #find mean and standard deviation for the variable
    mu = data.mean()
    sd = data.std()
    for x in data:
        z_score = (x - mu)/sd
    if abs(z_score) >= 2:
        print(f"{var}: {z_score}")

#No z-score is above the absoute value of 3 so no observations will be removed.

#CHECKING FOR NORMAL DISTRIBUTION
#look at data distribution with histograms with a normal distribution curve overlay
#continuous data 
cont_data = ["PPG", "oPPG", "pDIFF", "PACE", "dEFF", "eDIFF", "oEFF","WIN%", "SOS", "CONS", "A4F", "SAR"]

ncols = 4
nrows = int(np.ceil(len(cont_data)/ncols))
fig,axes = plt.subplots(nrows, ncols, figsize = (15,15))


for i, var in enumerate(cont_data):
    #plotting the histogram
    row = int(np.floor(i/ncols))
    col = i % ncols
    axes[row,col].hist(clean_data[var], density = True, alpha = 0.6, color = "green")
    axes[row,col].set_title(var, fontsize=10)
    axes[row,col].set_xlabel("Values")
    axes[row,col].set_ylabel("Probability")

    #plotting the probability density function (PDF)
    #fit normal distribution to each variable
    mean, sd = norm.fit(clean_data[var])
    #fit the min and max x values to each variable
    x = np.linspace(clean_data[var].min(), clean_data[var].max(), 100)
    p = norm.pdf(x, mean, sd)
    axes[row,col].plot(x, p, "k", linewidth = 2, color = "blue")

plt.show()
#The continuous variables appear to all have a fairly normal distribution


#CHECKING FOR COLLINEARITY
#correlation and causality 
#Identifying highly correlated variables (over 0.8) using a correlation matrix 

#dataframe to use - drop all non-continous variables
data_for_matrix = clean_data.drop(["TEAM", "CONF", "DIVISION", "GP", "RANKING", "W", "L"], axis=1)

#correlation matrix
corr_matrix = data_for_matrix.corr().abs()
print(corr_matrix)
#stack matrix values
stack_matrix = corr_matrix.stack().sort_values(ascending=False)
#remove correlation coefficient values that are 1
filter_matrix = stack_matrix.where(stack_matrix != 1).sort_values(ascending= False)
filter_matrix.head(25)

#remove eDIFF, pDIFF, SAR, dEFF due to high frequency of having a correlation coefficient 
#dropping win% since I will create a new ranking classifier to be the dependent variable

#updated matrix:
new_data_for_matrix = clean_data.drop(["TEAM", "CONF", "DIVISION", "GP", "RANKING", "W", "L", "WIN%", "pDIFF", "eDIFF", "dEFF", "SAR"], axis=1)
new_matrix = new_data_for_matrix.corr().abs()
#confirm that there are no correlations over 0.8
print(new_matrix.stack().sort_values(ascending=False))

#Dropping variables
clean_data = clean_data.drop(["pDIFF", "eDIFF", "dEFF", "SAR", "oPPG", "oEFF"], axis=1)

#Independent variables to include in prediction models: PPG, PACE, SAR, SOS, CONS, A4F
#Dependent variables that will be used: WIN% or Ranking classifier

#Creating a ranking classifier using the ranking column
#top 10 record - yes or no
top10 = []
for n in clean_data["RANKING"]:
    if n <= 10:
        top10.append("Y")
    else:
        top10.append("N")

clean_data["TOP10"] = top10

#drop original ranking column
clean_data = clean_data.drop(["RANKING"], axis=1)

#SAVE NEW DATA:
clean_data.to_csv("cleaned_team_stats.csv")
