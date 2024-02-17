# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()    # 종목명
    title = scrapy.Field()      # 제목
    date = scrapy.Field()       # 날짜
    text = scrapy.Field()    # 본문
    # source = scrapy.Field()     # 언론사
    # category = scrapy.Field()   # 카테고리
    # url = scrapy.Field()        # 기사링크

    pass
