import scrapy
import spacy
from collections import Counter
import requests
from scrapy.crawler import CrawlerProcess
import pandas as pd
from datetime import datetime

class ScrapeNewsSpider(scrapy.Spider):
    name = 'getnews'
    allowed_domains = ['www.boursorama.com/']
    fichier = open("links_lvmh.txt", "r")
    liste = fichier.readlines()
    for i in range(len(liste)):
        liste[i] = liste[i].replace('\n', '')
    start_urls=liste
    def parse(self, response):
       titre=response.xpath('normalize-space(//*[@id="main-content"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/h1/text())').get() #titre
       contenu=response.xpath('normalize-space(//*[@id="main-content"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[5])').get() #contenue
       date_str=response.xpath('//*[@id="main-content"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/h1/div/span[3]/text()').get()
       date_str=date_str[:10]
       date= datetime. strptime(date_str, '%d/%m/%Y').date()
       ch=titre+" "+contenu
       yield {
           'date': date,
           'Contenue': ch,
       }
process = CrawlerProcess(settings={
           "FEEDS": {
               "news_lvmh.json": {"format": "json"},
               "news_lvmh.csv": {"format": "csv"},
               # "items.jl": {"format": "jsonlines"},
           },
       })
process.crawl(ScrapeNewsSpider)
process.start()


