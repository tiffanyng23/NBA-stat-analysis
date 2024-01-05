import pandas as pd
import matplotlib.pyplot as plt
import statistics
from playerstats import SortPerformers
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

#DATASET
#NBA team statistics for 2022-2023 seasons
#already cleaned - steps shown in "data_clean_team.py"
clean_data = pd.read_csv("cleaned_team_stats.csv")
clean_data.head()

#standardize the data using StandardScalar
#variables have different scales, so the data will be standardized 

# variables: PPG, PACE, SOS, CONS, A4F

#creating new final_data variable to store scaled variables
scaled_data = clean_data

def scale_data(data, variable):
    """takes data, converts to an array and reshapes, and applies StandardScaler"""
    var_to_array = np.asarray(data[variable])
    reshaped_var = var_to_array.reshape(-1,1)
    scaled_variable = StandardScaler().fit_transform(reshaped_var)
    return scaled_variable

scaled_data["PPG"] = scale_data(scaled_data, "PPG")
scaled_data["PACE"] = scale_data(scaled_data, "PACE")
scaled_data["CONS"] = scale_data(scaled_data, "CONS")
scaled_data["SOS"] = scale_data(scaled_data, "SOS")
scaled_data["A4F"] = scale_data(scaled_data, "A4F")


#Convert top10 to a dummy variable
scaled_data.dtypes
scaled_data = pd.get_dummies(scaled_data, drop_first=True)

#LOGISTIC REGRESSION MODEL
#create x and y variables
y = scaled_data[["TOP10_Y"]]
x = scaled_data.iloc[:, :-1]

#split data in training and testing
x_train, x_test, y_train, y_test = \
    train_test_split(x, y, test_size=0.3, random_state=1234, stratify=y)
    
#instance of LogisticRegresison class
lr = LogisticRegression()
#applying fit method to fit the training data
lr.fit(x_train, y_train)

#applying predict method to predict y values
y_predict = lr.predict(x_test)

#ASSESSING MODEL
#confusion matrix
cm = confusion_matrix(y_test, y_predict)
score = lr.score(x_test, y_test)
    
#0.88 accuracy for predicting if a team finishes in the top 10 
#Since there are only 30 teams, the sample size is quite small. Will try to get more data over several seasons.