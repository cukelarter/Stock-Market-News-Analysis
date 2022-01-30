# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 00:38:41 2021

@author: cukel
"""

import pandas as pd
import numpy as np
import scrapy

df = pd.read_csv('C:/Users/cukel/OneDrive/Documents/PyScripts/hotshot finance type shit/health.csv')
tickers=list(df['Symbol'])
ticker=tickers[719]

ticker='OCGN'
class StocksSpider(scrapy.Spider):
    name = "stocks"
    
    def start_reqeusts(self):
        urls=[
            'https://www.nasdaq.com/market-activity/stocks/{}/press-releases'.format(ticker.lower())
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        page=response.url.split("/")
        filename=f'stocks-{page}.html'
        with open(filename,'wb') as f:
            f.write(response.body)