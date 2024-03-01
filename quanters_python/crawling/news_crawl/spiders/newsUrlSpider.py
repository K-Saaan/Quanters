from typing import Iterable
import scrapy
import time
import csv

from scrapy.http import Request
# from news_crawl.items import NewsCrawlItem, UrlCrawlItem
from ..items import NewsCrawlItem, UrlCrawlItem
from newspaper import Article
from datetime import datetime
import pandas as pd
import os

class NewsUrlSpider(scrapy.Spider):
    name = 'newsUrlCrawler'

    def start_requests(self):
        page = 1
        # 현재 날짜와 시간을 가져옵니다.
        now = datetime.now()
        except_out = 0
        # 년, 월, 일을 가져옵니다.
        pre_date = (now - pd.Timedelta(days=1)).strftime("%Y%m%d")
        curr_date = now.strftime("%Y%m%d")
        yymmdd = now.strftime("%Y%m%d")
        keywords = {'카카오주식':'035720', 'SK하이닉스':'000660', '네이버':'035420', '삼성전자':'005930'}
    
        for keyword in keywords.keys():
            for nowPage in range(1, page+1):
                try:
                    url_link = 'https://search.daum.net/search?nil_suggest=btn&w=news&DA=SBC&cluster=y&q=' + keyword + '&sd=' + pre_date + '153000' + '&ed=' + curr_date + '040000' +'&sort=accuracy&period=u&p=' + str(nowPage)
                    print("url : " + url_link)
                    yield scrapy.Request(url=url_link, callback=self.parse_news, meta={'keyword':keywords[keyword]})
                except Exception as e:
                    except_out += 1
                    if except_out > 100:
                        print('Url Crawl Exception : ' + e)
                    break

    # url 크롤링
    def parse_news(self, response):
        a = response.xpath('//*[@id="dnsColl"]/div[1]/ul')
    
        # for i in range(1, 11):
        for i in range(1, 2):
            num = str(i)
            print('now path : ', num, '>>>>>>>>>>>>>>>>>>')
            path = '//*[@id="dnsColl"]/div[1]/ul/li['+num+']'  
            
            sub = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[3]')
            # print('sub : ', sub)
            keyword = response.meta['keyword']

            if sub: # 기사 하단에 추가 더보기 및 추천 기사가 있는 경우
                # print('not null')
                title = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/text()').get()
                href = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/@href').get()    
            else: # 없는 경우
                # print(' null')
                title = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/text()').get()
                href = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/@href').get()

            print('keyword : ', keyword)
            print("title : ", title)
            print("href : ", href)
            
            item = UrlCrawlItem()
            item['company'] = keyword
            item['title'] = title
            item['url'] = href
            
            time.sleep(4)
                    
            yield item


class NewsSpider(scrapy.Spider):
    name = 'newsCrawler'

    def start_requests(self):
        # 현재 날짜와 시간을 가져옵니다.
        now = datetime.now()
        # 년, 월, 일을 가져옵니다.
        yymm = now.strftime("%Y%m")
        dd = now.strftime("%d")
        except_out = 0
        # url 수집 파일 읽어오기
        
        with open(f'/home/ubuntu/temp/quanters/data/news/url_crawl/{yymm}/url_{dd}.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    yield scrapy.Request(url=row['url'], callback=self.parse_news, meta={'company':row['company'], 'link':row['url']})
                except Exception as e:
                    except_out += 1
                    if except_out > 100:
                        print('Text Crawl Exception : ' + e)
                    break

    # 본문 크롤링
    def parse_news(self, response):
        article = Article(response.meta['link'], language='ko')
        article.download()
        article.parse()
        title = article.title
        text = article.text
        date = response.xpath('//*[@id="mArticle"]/div[1]/div[1]/span[2]/span/text()').get()
        company = response.meta['company']

        print('company : ', company)
        print('title : ', title)
        print('date : ', date)
        # print('text : ', text)
        
        item = NewsCrawlItem()
        item['company'] = company
        item['title'] = title
        item['date'] = date
        item['text'] = text

        time.sleep(5)

        yield item

            