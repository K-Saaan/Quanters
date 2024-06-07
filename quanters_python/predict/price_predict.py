import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from datetime import datetime
import xgboost as xgb
import logging
from path_check import isPath
import boto3
import io
import pickle
from .s3_connect import s3_connection

now  = datetime.now()
yyyymm = now.strftime("%Y%m")
dd = now.strftime("%d")

def save_file(df):
    # S3 클라이언트 생성
    s3 = s3_connection()
    print("s3 connected..")

    # S3에 업로드 할 로컬 파일 경로 (EC2)
    local_file_path = f"/home/kdh/quanters/data/predict/{yyyymm}/result_{dd}.csv"
    # 버킷명 (고정. 하드코딩)
    bucket_name = "quanter"
    # S3 업로드 파일 위치. 가장 루트 디렉토리는 / 이렇게 표시를 안하는듯.
    s3_file_path = f"{yyyymm}/result_{dd}.csv"
    s3.upload_file(local_file_path, bucket_name, s3_file_path)

    print("sftp put success..")


# /home/kdh/quanters/data/
def price_predict(sentiment_df, stock_df, yymm, dd):
    logging.info('Start price predict >>>>>>>>>>>>>>>>> ')
    # 감성분석 df와 주가 df를 불러온다.
    logging.info('sentiment df head : %s', sentiment_df.head())
    logging.info('stock df head : %s', stock_df.head())

    # predict()를 수행하기 위한 dataset을 만들기 위해 sentiment_df, stock_df를 병합한다.
    logging.info('sentiment df columns : %s', sentiment_df.columns)
    logging.info('stock df columns : %s', stock_df.columns)

    logging.info('sentiment df type : %s', sentiment_df.info())
    logging.info('stock df type : %s', stock_df.info())

    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    
    logging.info('sentiment df head : %s', sentiment_df.head())
    logging.info('stock df head : %s', stock_df.head())
    stock_df['date'] = sentiment_df['date']
    df = pd.merge(sentiment_df, stock_df, on=['date', 'company'], how='left')
    # predict()에 사용할 컬럼을 정의한다.
    logging.info('predict 컬럼 정의 df head : %s', df.head())
    df['company'] = df['company'].map({'카카오':0, 'SK하이닉스':1, '네이버':2, '삼성전자':3})
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['dayOfWeek'] = df['date'].dt.day_of_week

    x_features = ['company', 'Volume', 'sentiment', 'dayOfWeek', 'month', 'day']
    pred_df = df[x_features]
    logging.info('predict df head : %s', pred_df.head())

    # 모델 파일 경로
    model_path = '/home/kdh/quanters/model/price_predict/best_model.pkl'
    # 저장된 모델 불러오기
    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)

    # 예측을 수행한다.
    pred = loaded_model.predict(pred_df)
    #예측 결과를 pred_df['label']에 저장한다.
    pred_df['label'] = pred
    com_dict = {35720:'035720', 35420:'035420', 660:'000660', 5930:'005930'}
    pred_df['company'] = pred_df['company'].replace(com_dict)
    logging.info('predict df info : %s', pred_df.info())
    logging.info('predict df head : %s', pred_df.head())
    pred_path = f'/home/kdh/quanters/data/predict/{yymm}'
    isPath(pred_path)
    try:
        pred_df.to_csv(f'{pred_path}/result_{dd}.csv', index=False)
        save_file(pred_df)
    except Exception as e:
        logging.error(f'Price predict save_file Error : {e}')

    logging.info('End price predict >>>>>>>>>>>>>>>>> ')