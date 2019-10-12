import numpy as np # linear algebra
import pandas as pd # data processing
#from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn import ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
import pickle

filepath = ''
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
filename =filepath + 'rank_point_list.pkl'
rank_point_list1 = pickle.load(open(filename, 'rb'))
country_list = rank_point_list1.keys()

def predict1(home, away):
    if ((home not in country_list) or (away not in country_list)):
        return 'wrong country name'
    else:
      home_data = rank_point_list1[home]
      away_data = rank_point_list1[away]
      #print(home, away)
      ave_rank = (home_data[0] + away_data[0]) / 2
      rank_diff = home_data[0] - away_data[0]
      point_diff = home_data[1] - away_data[1]
      X =[[ave_rank, rank_diff, point_diff, False]]
      print(X)
      result = loaded_model.predict(X)
      if result == True:
          return home
      else:
          return away


# output ' Ture' means "Home team win.""
