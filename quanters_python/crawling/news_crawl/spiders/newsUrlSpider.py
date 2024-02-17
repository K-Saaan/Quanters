from typing import Iterable
import scrapy
import time
import csv

from scrapy.http import Request
from news_crawl.items import NewsCrawlItem
from newspaper import Article

class NewsUrlSpider(scrapy.Spider):
    name = 'newsUrlCrawler'

    def start_requests(self):
        page = 80
        startDate = ['20230601','20230608','20230615','20230622', '20230629', '20230706', '20230713','20230720', '20230727','20230803','20230810','20230817','20230824','20230831',
                    '20230907', '20230914', '20230921', '20230928', '20231005', '20231012', '20231019', '20231026', '20231102', '20231109', '20231116', '20231123']
        endDate = ['20230607', '20230614', '20230621', '20230628', '20230705', '20230712', '20230719', '20230726', '20230802', '20230809', '20230816', '20230823', '20230830',
                    '20230906', '20230913', '20230920', '20230927', '20231004', '20231011', '20231018', '20231025', '20231101', '20231108', '20231115', '20231122', '20231129']
        # startDate = ['20230601']
        # endDate = ['20230607']
        # keywords = ['카카오', 'SK하이닉스', '네이버']
        keywords = ['카카오주식']

        for keyword in keywords:
            for start, end in zip(startDate, endDate):
                for nowPage in range(1, page+1):
                    url_link = 'https://search.daum.net/search?nil_suggest=btn&w=news&DA=SBC&cluster=y&q=' + keyword + '&sd=' + start + '000000' + '&ed=' + end + '235959' +'&sort=accuracy&period=u&p=' + str(nowPage)
                    print("url : " + url_link)
                    yield scrapy.Request(url=url_link, callback=self.parse_news, meta={'keyword':keyword})


    def parse_news(self, response):
        a = response.xpath('//*[@id="dnsColl"]/div[1]/ul')
    
        for i in range(1, 11):
            num = str(i)
            print('now path : ', num, '>>>>>>>>>>>>>>>>>>')
            path = '//*[@id="dnsColl"]/div[1]/ul/li['+num+']'  
            
            sub = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[3]')
            # print('sub : ', sub)
            keyword = response.meta['keyword']

            if sub:
                # print('not null')
                title = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/text()').get()
                href = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/@href').get()    
            else:
                # print(' null')
                title = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/text()').get()
                href = a.xpath('//*[@id="dnsColl"]/div[1]/ul/li['+num+']/div[2]/div/div[1]/strong/a/@href').get()

            print('keyword : ', keyword)
            print("title : ", title)
            print("href : ", href)
            
            item = NewsCrawlItem()
            item['company'] = keyword
            item['title'] = title
            item['url'] = href
            
            time.sleep(1)
                    
            yield item


class NewsSpider(scrapy.Spider):
    name = 'newsCrawler'

    def start_requests(self):
        with open('../../data/news/newsUrlCrawl3.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield scrapy.Request(url=row['url'], callback=self.parse_news, meta={'company':row['company'], 'link':row['url']})

    
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

        time.sleep(2)

        yield item

            