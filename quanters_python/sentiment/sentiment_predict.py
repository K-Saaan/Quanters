import warnings
warnings.filterwarnings('ignore')

import os
import datetime
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import urllib.request
from path_check import isPath
import logging
import platform

import torch
import tensorflow as tf
from keras.models import load_model
import tensorflow_addons as tfa
# from tensorflow.keras.models import load_model
from transformers import BertTokenizer, TFBertForSequenceClassification, AdamW

tqdm.pandas()

os_name = platform.system()
if os_name == 'Darwin' :  # MacOS 
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
elif os_name == 'Windows' :
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
else :
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f'device : {device}')

def load_model(model_path):
    # 모델 전체 불러오기
    model_file_path = os.path.join(model_path, 'bert_model.pt')
    model = torch.load(model_file_path, map_location=device)
    # 상태 사전만 불러오기 (필요한 경우)
    state_dict_path = os.path.join(model_path, 'bert_model_state_dict.pt')
    model_state_dict = torch.load(state_dict_path, map_location=device)
    model.load_state_dict(model_state_dict)
    return model

# 모델과 tokenizer 선언
# model_path = '/home/kdh/quanters/model/sentiment_predict/best_model.h5'
MODEL_NAME = "klue/bert-base"
model_path = '/home/kdh/quanters/model/sentiment_predict'
model = load_model(model_path)
optimizer = AdamW(model.parameters(), lr=5e-5)
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

# 기업별 감성분석 점수의 평균을 구한다.
def sentiment_of_day(df, holiday_list):
    sentiment_list = []
    dates = []
    com_list = []
    company_list = ['035720', '035420', '000660', '005930']
    for com in company_list:
        df_company = df[df['company'] == com]
        
        sentiment_list.append(round(df_company['sentiment'].mean(), 3))
        com_list.append(com)

    df1 = pd.DataFrame(com_list, columns=['company'])
    df2 = pd.DataFrame(sentiment_list, columns=['sentiment'])
    sen_df = pd.concat([df1, df2], axis=1)

    return sen_df


def predict(model, tokenizer, text, device=device):
    """
    불러온 모델을 사용하여 텍스트 데이터에 대한 예측을 수행하는 함수
    """
    model.eval()  # 모델을 평가 모드로 설정
    model.to(device)
    
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    pred = torch.sigmoid(logits)
    predictions = torch.argmax(pred, dim=-1)

    return predictions.item()


def sentiment_predict(news_df, day_list, holiday_list):
    logging.info('Start sentiment analysis >>>>>>>>>>> ')
    logging.info('news_df head : %s', news_df.head())

    com_dict = {35720:'035720', 35420:'035420', 660:'000660', 5930:'005930'}
    news_df['company'] = news_df['company'].replace(com_dict)
    news_df.dropna(axis=0, inplace=True)
    news_df['sentiment'] = news_df['text'].progress_apply(lambda x: predict(model, tokenizer, x, device))
    
    # 'sentiment' 결과 확인
    logging.info('news_df head : %s', news_df.head())
    
    news_df.set_index('date', inplace=True)
    news_df.sort_index(ascending=True, inplace=True)

    date = day_list[-1].replace('-', '')
    yyyymm = date[:6]
    dd = date[6:]
    sentiment_df = sentiment_of_day(news_df, holiday_list)
    logging.info('sentiment df columns : %s', sentiment_df.columns)
    logging.info('sentiment df head : %s', sentiment_df.head())
    sentiment_df['date'] = day_list[0]
    sentiment_path = f'/home/kdh/quanters/data/sentiment/{yyyymm}'
    isPath(sentiment_path)
    sentiment_df.to_csv(f'{sentiment_path}/sentiment_df_{dd}.csv', index=False)
    logging.info('End sentiment analysis >>>>>>>>>>> ')
    return sentiment_df

