import scrapy
from datetime import datetime
import pandas as pd
import sqlite3


location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActionsTotal.sqlite'
db = sqlite3.connect(location)
Date=pd.read_sql_query('select min (Date)  from Action',db).iat[0,0]
date_min= datetime. strptime(Date, '%Y-%m-%d').date()



class ScrapeTableSpider(scrapy.Spider):
    name = 'geturl'
    allowed_domains = ['www.boursorama.com/cours/actualites/']
    base_url = 'https://www.boursorama.com'
    start_urls = ['https://www.boursorama.com/cours/actualites/1rPTTE/page-'+str(i+1) for i in range(145)]
    ch=''
    def parse(self, response):
        fichier = open("links_total.txt", "w")
        rows=response.xpath('//*[@id="main-content"]/div/section[1]/div[2]/article/div[2]/div[2]/div[1]/div[2]/ul/li')
        for row in rows:
            link=row.xpath('div[1]/a//@href').get()
            Date=row.xpath('div[3]/div/span/span[3]/text()').get()
            date= datetime. strptime(Date, '%d.%m.%Y').date()
            if (date>=date_min):
                yield {
                    'date':date,
                    'link':link,
                }
                self.ch=self.ch+self.base_url+link+'\n'
        fichier.write(self.ch)



