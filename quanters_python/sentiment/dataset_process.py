import pandas as pd
import re
import datetime
import FinanceDataReader as fdr

# path에 있는 뉴스 크롤링 파일 열기
path = './data/news/'
kakao_news = pd.read_csv(path + 'kakaoNewsCrawl.csv') # 035720
naver_news = pd.read_csv(path + 'naverNewsCrawl.csv') # 035420
sk_news = pd.read_csv(path + 'skNewsCrawl.csv') # 000660
samsung_news = pd.read_csv(path + 'newsCrawl.csv') # 005930

# company를 기업 코드로 변경
kakao_news['company'] = '035720'
naver_news['company'] = '035420'
sk_news['company'] = '000660'
samsung_news['company'] = '005930'

# 기업별 뉴스 크롤링 df를 병합하여 df_news에 저장한다.
df_news = pd.concat([kakao_news, naver_news, sk_news,samsung_news])

df_news['date'] = pd.to_datetime(df_news['date'])

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
    # 특수기호 제거
    df['text'] = df['text'].apply(lambda x: re.sub('[■▷▶]', '', x) if isinstance(x, str) else x)
    # 보도사 제거
    df['text'] = df['text'].apply(remove_news_name)

    return df

df_news = news_process(df_news)

# 전처리한 뉴스 데이터 저장
df_news.to_csv('./data/news/final_news_dataset.csv', index=False)

# target_date의 기업별 주가 데이터를 수집해 df로 저장
stocks = ['035720', '035420', '000660', '005930']
stock_data = []
target_date = '2024-02-05'
for stock in stocks:
    data = fdr.DataReader(stock, start=target_date, end=target_date)
    data['company'] = stock
    stock_data.append(data)

stock_df = pd.concat(stock_data)

stock_df = stock_df.rename(columns={'Date':'date'})
stock_df['date'] = pd.to_datetime(stock_df['date'])

# 전처리한 주가 데이터 저장
stock_df.to_csv('./data/news/final_stock_dataset.csv', index=False)