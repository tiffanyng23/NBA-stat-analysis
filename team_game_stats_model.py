import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_predict



#DATASET: Average season statistics for each team from 2018-2023. 
#This includes data from every team for 5 NBA seasons, with each row representing one team's performance in 1 season.
#Source: https://www.basketball-reference.com/leagues/NBA_2023.html#per_game-team

#Dataset has been cleaned, steps shown in "Data_clean_Game_Stats_2018_2023.py"

#CLEAN VERSION
cleaned_data = pd.read_csv("cleaned_game_stats.csv")
cleaned_data.head()


#DATA PREPARATION FOR PREDICTION MODELS

#Standardize data using StandardScaler:
def scale_data(data, variable):
    """takes data, converts to an array and reshapes, and applies StandardScaler"""
    var_to_array = np.asarray(data[variable])
    reshaped_var = var_to_array.reshape(-1,1)
    scaled_variable = StandardScaler().fit_transform(reshaped_var)
    return scaled_variable

to_scale_data = cleaned_data.drop(["Rk", "Team", "G", "MP", "Year"], axis = 1)

var_to_scale = ['FGA', 'FG%', '3P', '3P%', '2P', '2P%', 'FT', 'FT%', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

for var in var_to_scale:
    #apply scale_data function
    to_scale_data[var] = scale_data(to_scale_data, var)

#CREATING DUMMY VARIABLES
#Convert Top10 variable to a dummy variable so it can be used in prediction models
to_scale_data.dtypes
final_data = pd.get_dummies((to_scale_data), drop_first=True)

#APPLYING PREDICTION MODELS

#LOGISTIC REGRESSION
#create x and y variables
x = final_data.iloc[:, :-1]
y = final_data[["Top10_Y"]]

#split data in training and testing
#stratify by y to ensure equal splitting of each outcome between each group
x_train, x_test, y_train, y_test = \
    train_test_split(x, y, test_size=0.3, random_state=1234, stratify=y)
    
#instance of Logistic regression class
lr = LogisticRegression()

#applying the fit method 
#training the model using the training data
lr.fit(x_train, y_train)

#applying the predict method to predict y values using the test group
y_predict = lr.predict(x_test)

#ASSESSING MODEL
#confusion matrix
results_matrix = confusion_matrix(y_test, y_predict)
#r squared (Accuracy)
r_squared = lr.score(x_test, y_test)
# R-squared of 0.84, indicates a good model that predicted 84% of the cases correctly.

#Find sensitivity and specificity
TP = results_matrix[1,1]
TN = results_matrix[0,0]
FP = results_matrix[0,1]
FN = results_matrix[1,0]

#Sensitivity (True positive -identifying teams that had a top 10 regular season record)
sensitivity = TP/(TP+FN)
#The sensitivity is 0.67, so the model identified 67% of the top 10 teams

#specificity (True negative -teams that did not have a top 10 regular season record)
specificity = TN/(TN + FP)
#The specificity is 0.93, so the model identified 93% of the teams that did not have a top 10 record.


#Cross Validation
#I will create more models using cross validation to partition the data.
#I will put 7 folds, so the data will be divided into 7 subsets/folds.
#Training set will be 6 fold, testing will be 1 fold.

#logistic regression
logisticregression = LogisticRegression(random_state=123)

cv_result_lr = cross_validate(logisticregression, x, y, cv=7, 
                              scoring= "roc_auc", return_train_score = True)

#comparing prediced and actual y values, creating confusion matrix 
y_predict_cv = cross_val_predict(logisticregression, x, y, cv=7)
conf_matrix = confusion_matrix(y,y_predict_cv)

#AUC
lr_auc = np.average(cv_result_lr["test_score"])


#confusion matrix
TP_2 = conf_matrix[1,1]
TN_2 = conf_matrix[0,0]
FP_2 = conf_matrix[0,1]
FN_2 = conf_matrix[1,0]

#Sensitivity (True positive -identifying teams that had a top 10 regular season record)
sensitivity_cv = TP_2/(TP_2+FN_2)
#The sensitivity is 0.67, so the model identified 67% of the top 10 teams

#specificity (True negative -teams that did not have a top 10 regular season record)
specificity_cv = TN_2/(TN_2 + FP_2)

#Summary
#By using logistic regression (both using one training and testing set and with cross validation), a top 10 regular season performance can be predicted.
# Cross validated logistic regression model: 0.94 AUC
# Sensitivity of 0.78 (ability to predict teams that finish in the top 10 record) 
# Specificity of 0.89 (ability to predict teams that did not finish with a top 10 record).


