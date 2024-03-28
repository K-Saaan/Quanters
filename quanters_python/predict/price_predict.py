import pandas as pd
from datetime import datetime
from autogluon.tabular import TabularDataset, TabularPredictor
import logging
from path_check import isPath
import boto3
import io
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

    # predict()를 수행하기 위한 dataset을 만들기 위해 sentiment_df, stock_df를 병합한다.
    logging.info('sentiment df columns : %s', sentiment_df.columns)
    logging.info('stock df columns : %s', stock_df.columns)

    logging.info('sentiment df type : %s', sentiment_df.info())
    logging.info('stock df type : %s', stock_df.info())
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    logging.info('sentiment df head : %s', sentiment_df.head())
    logging.info('stock df head : %s', stock_df.head())
    df = pd.merge(sentiment_df, stock_df, left_on=['date', 'company'], right_on=['date', 'company'])
    # predict()에 사용할 컬럼을 정의한다.
    x_features = ['company', 'date', 'sentiment', 'Volume']

    pred_df = df[x_features]
    logging.info('predict df head : %s', pred_df.head())
    # TabularDataset으로 변경해준다.
    pred_set = TabularDataset(df[x_features])
    # 사전에 학습된 predictor를 불러온다.
    predictor = TabularPredictor.load('/home/kdh/quanters/model/price_predict/', require_py_version_match=False)
    # 예측을 수행한다.
    pred = predictor.predict(pred_set)
    #예측 결과를 pred_df['label']에 저장한다.
    pred_df['label'] = pred
    com_dict = {35720:'035720', 35420:'035420', 660:'000660', 5930:'005930'}
    pred_df['company'] = pred_df['company'].replace(com_dict)
    logging.info('predict df info : %s', pred_df.info())
    logging.info('predict df head : %s', pred_df.head())
    pred_path = f'/home/kdh/quanters/data/predict/{yymm}'
    isPath(pred_path)
    try:
        save_file(pred_df)
        pred_df.to_csv(f'{pred_path}/result_{dd}.csv', index=False)
    except Exception as e:
        logging.error(f'Price predict save_file Error : {e}')

    logging.info('End price predict >>>>>>>>>>>>>>>>> ')