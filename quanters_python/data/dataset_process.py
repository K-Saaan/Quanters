import pandas as pd
import re
import datetime
import os
import FinanceDataReader as fdr
import logging
from path_check import isPath

# 내용에 보도사가 있으면 제거한다.
def remove_news_name(row):
    news_lists = ['네이버 뉴스', '다음 뉴스', '조선일보', '동아일보', '한겨레', '경향신문', '중앙일보', '매일경제', '서울신문', '한국일보', 
                '머니투데이', '아시아경제', 'YTN', 'SBS 뉴스', 'KBS 뉴스', 'MBC 뉴스', 'JTBC 뉴스', '채널A 뉴스', 'TV조선 뉴스', '오마이뉴스']
    for news_list in news_lists:
        if news_list in row:
            return ''
    return row

# 본문 내용에서 불용어를 제거한다.
def news_process(df):
    # 결측치 제거
    df.dropna(inplace=True)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{2}-\d{3}-\d{4}\b'
    link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    reporter_pattern = r'\b\w+기자\b|\b\w+ 기자\b'
    
    # 크롤링으로 함께 수집된 '\n' 제거 / 이메일, 전화번호, 링크, 기자 이름 등 제거
    df['text'].replace('\n', '', regex=True)
    df['text'] = df['text'].str.replace(email_pattern, '')
    df['text'] = df['text'].str.replace(phone_pattern, '')
    df['text'] = df['text'].str.replace(link_pattern, '')
    df['text'] = df['text'].str.replace(reporter_pattern, '')
    df['text'] = df['text'].apply(lambda x: re.sub('[^A-Za-z0-9가-힣]', ' ', x))
    df['text'] = df['text'].apply(lambda x: re.sub(' +', ' ', x))
    # 특수기호 제거
    df['text'] = df['text'].apply(lambda x: re.sub('[■▷▶]', '', x) if isinstance(x, str) else x)
    # 보도사 제거
    df['text'] = df['text'].apply(remove_news_name)

    return df

def combine_df(day_list):
    # 데이터프레임 리스트
    day_list = day_list[:-1]
    df_list = []
    for date in day_list:
        # 년월, 일자 추출
        date = date.replace('-', '')
        yyyymm = date[:6]
        dd = date[6:]
        # 파일 경로 생성
        filepath = f'/home/kdh/quanters/data/news/text_crawl/{yyyymm}/text_{dd}.csv'
        
        # CSV 파일 읽기
        df = pd.read_csv(filepath)
        
        # 데이터프레임 리스트에 추가
        df_list.append(df)

    # 데이터프레임 합치기
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df


def data_preprocess(day_list):
    logging.info(' Start data preprocess >>>>>>>>>> ')

    # day_list의 날짜에 있는 csv 파일을 가져와서 하나로 합친다.
    try:
        df_news = combine_df(day_list)
    except Exception as e:
        logging.error('combine df Error : ', e)

    # path에 있는 뉴스 크롤링 파일 열기

    # company를 기업 코드로 변경

    # 기업별 뉴스 크롤링 df를 병합하여 df_news에 저장한다.
    df_news['date'] = pd.to_datetime(df_news['date'])

    # 본문 내용 전처리
    df_news = news_process(df_news)

    day_list[-1].replace('-', '')
    yyyymm = day_list[-1].replace('-', '')[:6]
    dd = day_list[-1].replace('-', '')[6:]
    news_path = f'/home/kdh/quanters/data/process_data/news/{yyyymm}'
    # path가 없으면 생성
    isPath(news_path)

    # 전처리한 뉴스 데이터 저장
    df_news.to_csv(f'{news_path}/process_news_dataset_{dd}.csv', index=False)

    # target_date의 기업별 주가 데이터를 수집해 df로 저장
    stocks = ['035720', '035420', '000660', '005930']
    stock_data = []
    target_date = day_list[-1]
    for stock in stocks:
        data = fdr.DataReader(stock, start=target_date, end=target_date)
        data['company'] = stock
        stock_data.append(data)

    stock_df = pd.concat(stock_data)
    stock_df.reset_index
    stock_df.reset_index(inplace=True)
    stock_df = stock_df.rename(columns={'Date':'date'})
    logging.info('stock df columns : %s', stock_df.columns)
    stock_path = f'/home/kdh/quanters/data/process_data/stock/{yyyymm}'
    isPath(stock_path)

    # 전처리한 주가 데이터 저장
    stock_df.to_csv(f'{stock_path}/process_stock_dataset_{dd}.csv' , index=False)
    logging.info('End  data preprocess >>>>>>>>>>>>>>>> ')
    return stock_df, df_news