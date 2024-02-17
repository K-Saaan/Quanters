import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import roc_auc_score, roc_curve, mean_squared_log_error, r2_score, mean_squared_error, confusion_matrix
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingRegressor, HistGradientBoostingRegressor, GradientBoostingRegressor,RandomForestRegressor,ExtraTreesRegressor
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, train_test_split, RepeatedStratifiedKFold, cross_val_predict,cross_val_score
from autogluon.tabular import TabularDataset, TabularPredictor


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 감성분석 df와 주가 df를 불러온다.
sentiment_df = pd.read_csv('./data/sentiment/sentiment_df.csv', index=False)
stock_df = pd.read_csv('./data/news/final_stock_dataset.csv', index=False)

# predict()를 수행하기 위한 dataset을 만들기 위해 sentiment_df, stock_df를 병합한다.
df = pd.merge(sentiment_df, stock_df, left_on=['date', 'company'], right_on=['date', 'company'])

# predict()에 사용할 컬럼을 정의한다.
x_features = ['company', 'date', 'sentiment', 'Volume']

pred_df = df[x_features]

# TabularDataset으로 변경해준다.
pred_set = TabularDataset(df[x_features])
# 사전에 학습된 predictor를 불러온다.
predictor = TabularPredictor.load('./model/price_predict/model.pkl')
# 예측을 수행한다.
pred = predictor.predict(pred_set)
#예측 결과를 pred_df['label']에 저장한다.
pred_df['label'] = pred

pred_df.to_csv('./data/predict/pred_df.csv')


