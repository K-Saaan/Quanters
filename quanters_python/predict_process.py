import os
from datetime import datetime, date, timedelta
import subprocess
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from crawling.news_crawl.spiders.newsUrlSpider import NewsUrlSpider
from crawling.news_crawl.spiders.newsUrlSpider import NewsSpider
from twisted.internet import reactor

from data.dataset_process import data_preprocess
from predict.price_predict import price_predict
from sentiment.sentiment_predict import sentiment_predict
from path_check import isPath

import time
import logging

now = datetime.now()
yymm = now.strftime("%Y%m")
dd = now.strftime("%d")
today = now.strftime("%Y-%m-%d")

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.DEBUG)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log를 console에 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
log_now = now.strftime("%Y%m%d%H%M%S")
log_path = f'/home/kdh/quanters/log/{yymm}'
isPath(log_path)
file_handler = logging.FileHandler(f'{log_path}/{log_now}_process.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info(f'today : {now}')

def run_crawl(spider_name):
    print(f"Starting crawl for {spider_name}")
    subprocess.run(["scrapy", "crawl", spider_name])
    print(f"Finished crawl for {spider_name}")

crawl_file_path = f'/home/kdh/quanters/data/news/url_crawl/{yymm}/url_{dd}.csv'
if not os.path.exists(crawl_file_path):
    logging.info('crawl_file_path is already exist')
    run_crawl('newsUrlCrawler')
    time.sleep(60)
    run_crawl('newsCrawler')
else:
    logging.info('crawl file already exsist')

# 전날 폐장부터 오늘 개장 전까지의 뉴스를 감성분석 해 오늘의 주가 등하락을 예측
# 학습 : 뉴스 감성분석 결과 + 전날 거래량 | 오늘 주가 결과

# 화요일 개장의 주가를 알기 위해서는 전날 폐장 이후부터 개장 전까지의 데이터 필요
# ex 월요일 15시 30분부터 화요일 04시까지 데이터 크롤링 화요일 날짜로 저장(당일)
# 월요일이 1일 화요일이 2일인 경우 수집 파일은 2일.csv로 저장

def is_first_day(now, holiday_day_list):
    today = now.strftime("%Y-%m-%d")
    day_list = []
    if today in holiday_day_list:
        return 0
    
    day_list = []
    day_list.append(today)
    pre_date = now - pd.Timedelta(days=1)
    while pre_date in holiday_day_list:
        day_list.append(pre_date.strftime("%Y-%m-%d"))
        pre_date -= pd.Timedelta(days=1)
    day_list.append(pre_date.strftime("%Y-%m-%d"))
    return day_list

# 지정한 해의 영업일과 휴일이 저장된 df 출력
working_day_df = pd.read_csv('/home/kdh/quanters/data/working_day/working_day.csv')
holiday_day_list = working_day_df.loc[working_day_df['working_day'] == 0, 'date'].to_list()


day_list = is_first_day(now, holiday_day_list)

if day_list != 0: # 영업일인 경우 수행
    stock_df, df_news = data_preprocess(day_list)
    sentiment_df = sentiment_predict(df_news, day_list, holiday_day_list)
    price_predict(sentiment_df, stock_df, yymm, dd)


