import os
import datetime
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import urllib.request
import seaborn as sns
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model
from transformers import BertTokenizer, TFBertForSequenceClassification

# 전처리한 뉴스 데이터셋 불러오기
news_df = pd.read_csv('./data/news/final_news_dataset.csv', index=False)

# 모델과 tokenizer 선언
model_path = './model/sentiment_predict/best_model.h5'
load_model = load_model(model_path, custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})
tokenizer = BertTokenizer.from_pretrained("klue/bert-base")

# 입력 데이터(문장) 길이 제한
MAX_SEQ_LEN = 128

# 텍스트를 학습 가능한 데이터로 변환
def convert_data_x(X_data):
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

data_x = convert_data_x(news_df['text'])

# 텍스트 감성분석 수행
text_pred = load_model.predict(data_x)
# 가장 확률이 높은 감성을 반환
text_pred = np.argmax(text_pred, axis=1)
# 'sentiment' 컬럼에 감성분석 결과 저장
news_df['sentiment'] = text_pred

# 공휴일 계산을 하기 위한 공휴일 리스트
holidays = pd.to_datetime([
    '2023-01-01',  # 신정
    '2023-01-22',  # 설날
    '2023-01-23',  # 설날
    '2023-01-24',  # 설날
    '2023-03-01',  # 삼일절
    '2023-05-01',  # 노동절
    '2023-05-05',  # 어린이날
    '2023-06-06',  # 현충일
    '2023-08-15',  # 광복절
    '2023-09-29',  # 추석
    '2023-09-30',  # 추석
    '2023-10-01',  # 추석
    '2023-10-03',  # 개천절
    '2023-10-09',  # 한글날
    '2023-12-25'   # 크리스마스
    '2024-01-01',  # 신정
    '2024-02-10',  # 설날
    '2024-02-11',  # 설날
    '2024-02-12',  # 설날
    '2024-03-01',  # 삼일절
    '2024-04-10',  # 국회의원 선거
    '2024-05-05',  # 어린이날
    '2024-05-06',  # 대체 공휴일
    '2024-05-15',  # 부처님 오신 날
    '2024-06-06',  # 현충일
    '2024-08-15',  # 광복절
    '2024-09-16',  # 추석
    '2024-09-17',  # 추석
    '2024-09-18',  # 추석
    '2024-10-03',  # 개천절
    '2024-10-09',  # 한글날
    '2024-12-25',  # 크리스마스
])

# 최근 영업일의 폐장부터 대상일 개장전까지의 감성점수 평균을 구한다.
def sentiment_of_day(df):
    # collected_row = []
    sentiment_list = []
    day_list = []
    com_list = []
    company_list = ['035720', '035420', '000660', '005930']
    for com in company_list:
        df_company = df[df['company'] == com]
        unique_days = pd.to_datetime(df_company.index.date).unique()
        # 개장 전까지의 데이터 수집
        for date in tqdm(unique_days):
            # 첫 번째 날 제외
            if date == unique_days.min():
                continue
            # 주말이나 공휴일 제외
            if date.weekday() >= 5 or date in holidays:
                continue
            # 가장 최근 영업일 조회
            pre_date = date - pd.Timedelta(days=1)
            while pre_date.weekday() >= 5 or pre_date in holidays:
                pre_date -= pd.Timedelta(days=1)

            start_time = pd.Timestamp(pre_date.year, pre_date.month, pre_date.day, 15, 30)
            end_time = pd.Timestamp(date.year, date.month, date.day, 8, 59)
            sentiment_list.append(round(df_company.loc[start_time:end_time, 'sentiment'].mean(), 3))
            day_list.append(date)
            com_list.append(com)

    df1 = pd.DataFrame(sentiment_list, columns=['sentiment'])
    df2 = pd.DataFrame(day_list, columns=['date'])
    df3 = pd.DataFrame(com_list, columns=['company'])
    sen_df = pd.concat([df3, df2, df1], axis=1)

    return sen_df

news_df.set_index('datetime', inplace=True)
news_df.sort_index(ascending=True, inplace=True)
sentiment_df = sentiment_of_day(news_df)

sentiment_df.to_csv('./data/sentiment/sentiment_df.csv', index=False)

