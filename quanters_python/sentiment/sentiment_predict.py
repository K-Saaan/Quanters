import os
import datetime
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import urllib.request
from path_check import isPath
import logging

import tensorflow as tf
from keras.models import load_model
import tensorflow_addons as tfa
# from tensorflow.keras.models import load_model
from transformers import BertTokenizer, TFBertForSequenceClassification

# 모델과 tokenizer 선언
model_path = '/Users/gimsan/Documents/GitHub/Quanters/quanters_python/model/sentiment_predict/best_model.h5'
model = load_model(model_path, custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})
tokenizer = BertTokenizer.from_pretrained("klue/bert-base")

# 텍스트를 학습 가능한 데이터로 변환
def convert_data_x(X_data):

    # 입력 데이터(문장) 길이 제한
    MAX_SEQ_LEN = 128
    
    # BERT 입력으로 들어가는 token, mask, segment, target 저장용 리스트
    tokens, masks, segments= [], [], []
    
    for  X in tqdm(X_data):
        # token: 입력 문장 토큰화
        token = tokenizer.encode(X, truncation = True, padding = 'max_length', max_length = MAX_SEQ_LEN)
        
        # Mask: 토큰화한 문장 내 패딩이 아닌 경우 1, 패딩인 경우 0으로 초기화
        num_zeros = token.count(0)
        mask = [1] * (MAX_SEQ_LEN - num_zeros) + [0] * num_zeros
        
        # segment: 문장 전후관계 구분: 오직 한 문장이므로 모두 0으로 초기화
        segment = [0]*MAX_SEQ_LEN

        tokens.append(token)
        masks.append(mask)
        segments.append(segment)

    # numpy array로 저장
    tokens = np.array(tokens)
    masks = np.array(masks)
    segments = np.array(segments)

    return [tokens, masks, segments]

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

def sentiment_predict(news_df, day_list, holiday_list):
    # 전처리한 뉴스 데이터셋 불러오기
    # news_df = pd.read_csv('./data/news/final_news_dataset.csv', index=False)
    logging.info('Start sentiment analysis >>>>>>>>>>> ')
    data_x = convert_data_x(news_df['text'])

    # 텍스트 감성분석 수행
    text_pred = model.predict(data_x)
    # 가장 확률이 높은 감성을 반환
    text_pred = np.argmax(text_pred, axis=1)
    # 'sentiment' 컬럼에 감성분석 결과 저장
    news_df['sentiment'] = text_pred
    # logging.info('news_df columns : ', news_df.columns)
    
    news_df.set_index('date', inplace=True)
    news_df.sort_index(ascending=True, inplace=True)

    date = day_list[-1].replace('-', '')
    yyyymm = date[:6]
    dd = date[6:]
    sentiment_df = sentiment_of_day(news_df, holiday_list)
    logging.info('sentiment df columns : %s', sentiment_df.columns)
    sentiment_df['date'] = day_list[0]
    sentiment_path = f'/home/ubuntu/temp/quanters/data/sentiment/{yyyymm}'
    isPath(sentiment_path)
    sentiment_df.to_csv(f'{sentiment_path}/sentiment_df_{dd}.csv', index=False)
    logging.info('End sentiment analysis >>>>>>>>>>> ')
    return sentiment_df

