import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm

#DATASET: Average season statistics for each team from 2018-2023. 
#Source: https://www.basketball-reference.com/leagues/NBA_2023.html#per_game-team

team_data = pd.read_csv("team_stats_2018_2023.csv")
team_data.head()


#DATA CLEANING
team_data_copy = team_data

team_data_copy.head()
team_data_copy.tail()

#check for missing data/rows
#No missing values shown using isnull method in any column
team_data_copy.isnull().sum()

#set of all teams
result = set()
for x in team_data_copy["Team"]:
    result.add(x)
print(result)

#EXPLORTORY DATA ANALYSIS:
#Summary Statistics
round(team_data_copy.describe(),2)

#IDENTIFY OUTLIERS:
#Creating Boxplots to identify outliers and to visualize percentile statistics:

#List of boxplot variables
bp_variables = []
for col in team_data_copy.columns:
    if (col != 'Rank') and (col !='Team') and (col !='G') and (col !='MP') and (col != "Year"):
        bp_variables.append(col)
print(bp_variables)

#21 variables
len(bp_variables)

#Visualization Using Boxplots
num_cols = 5
num_rows = int(np.ceil(len(bp_variables)/num_cols))

fig,axes = plt.subplots(num_rows, num_cols, figsize=(20,15))
for i, var in enumerate(bp_variables):
    row = int(np.floor(i/num_cols))
    col = i % num_cols
    axes[row,col].boxplot(team_data_copy[var], patch_artist=True,
            boxprops=dict(facecolor="green", color="black", linewidth=2),
            whiskerprops=dict(color="black", linewidth=2), 
            medianprops=dict(color="black", linewidth=1), 
            capprops=dict(color="black", linewidth=2),
            flierprops=dict(markerfacecolor="blue", marker="o", markersize=7))
    axes[row,col].set_title(var)
plt.tight_layout()
plt.show()
#There appears outliers present in many of the variables. 
# Will calculate z-scores for each point. If the standard deviation of any value is over 3, then I will remove it.

#Calculating z score for all the points for variables in the boxplots.
#Formula: z = (x-mu)/sigma

for var in bp_variables:
    data = team_data_copy[var]
    mu = data.mean()
    sd = data.std()
    for x in data:
        z_score = (x - mu)/sd
    if abs(z_score) >= 2:
        print(f"{var}: {z_score}")

#After checking the z-scores for every observation in every variable, there are no z-scores over 3 and only three z-scores over 2.
#These are values that resulted from a team's performance over the course of 1 season so they depend on team performance and are not due to calculation errors.
#Therefore, I will not remove any observations.

#CHECKING FOR NORMAL DISTRIBUTION:
#Creating histograms with an overlay of a probability density function

#Plotting the histogram + probability density function
ncols = 5
nrows = int(np.ceil(len(bp_variables)/ncols))
fig, axes = plt.subplots(nrows, ncols, figsize=(20,15))

for i, var in enumerate(bp_variables):
    #histogram
    row = int(np.floor(i/ncols))
    col = i % ncols
    axes[row,col].hist(team_data_copy[var], density = True, bins = 15, alpha = 0.6, color = "pink")
    axes[row,col].set_title(var, fontsize=10)

    #PDF
    #fit normal distribution specifically to each variable
    mean, sd = norm.fit(team_data_copy[var])
    #fit the min and max x values specifically to each variable
    x = np.linspace(team_data_copy[var].min(), team_data_copy[var].max(), 100)
    p = norm.pdf(x, mean, sd)
    axes[row,col].plot(x, p, "k", linewidth = 2, color = "blue")

plt.tight_layout()
plt.show()

#All variables appear to have a normal distribution. 
# Therefore, no variable data needs to be transformed.

#CHECKING FOR COLLINEARITY:
#Correlation Coefficient Matrix
#check for correlation coefficients and remove highly correlated variables (over 0.8)
matrix_data = team_data_copy[bp_variables]
matrix = matrix_data.corr().abs()
print(matrix)

#correlation heatmap
plt.figure(figsize=(8,6))
a = sns.heatmap(data=matrix, cmap=sns.cubehelix_palette(as_cmap=True))
a.set_title("Correlation Heatmap", fontsize = 12)

plt.tight_layout()
plt.show()
#Visualization of correlation between variables - there are so many variables.
#So I will need to filter for variables with high correlations and look closely at those!



#stack matrix values + sort by descending order
matrix_2 = matrix.stack()
filter_matrix = matrix_2.where(matrix_2 != 1).sort_values(ascending = False)
len(filter_matrix)
#441 rows - this is too long! Filter for those with a correlation of over 0.8
filter_matrix.head(40)
#remove 3PA - 3 correlations over 0.8, 2PA - 2 correlations over 0.8, remove FG - 2 correlations over 0.8
#FTA, DRB will also be removed since each of them also had 1 correlation over 0.8

#Dropping variables with a high correlation coefficient
team_data_copy = team_data_copy.drop(["3PA", "2PA", "FG", "FTA", "DRB"], axis = 1)
cleaned_data = team_data_copy


#CREATE A TOP 10 RANKING CATEGORY:
#Add a Top10 column to identify which team finished with a top 10 record league-wide in each season
#I chose to do Top 10 regular season record regardless of conference since conference strength varies by season.
#For example, the West could have more strong teams in one season and in another, the East could have more.
#Also, since the play-in tournament was added in 2020, teams with a conference ranking of 7-10 are not guaranteed a playoff spot.
#This makes it more complicated to employ a conference-based rank classifier that stratifies for a true playoff team.
#The play-in tournament could lead to 10th conference ranked team to make the playoffs over a 7th ranked team. 

#Finishing with a top 10 league-wide record HIGHLY LIKELY means that your team is a playoff team that also has a strong/winning record.

#This will be the outcome that will be used in the prediction models

top10 = []
for x in cleaned_data["Rk"]:
    if x <=10:
        x = "Y"
        top10.append(x)
    else:
        x = "N"
        top10.append(x)

cleaned_data["Top10"] = top10

#confirming top10 was added correctly
cleaned_data.head(15)

#SAVING NEW DATASET
cleaned_data.to_csv("cleaned_game_stats.csv", index=False)
