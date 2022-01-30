# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 21:09:16 2021

@author: cukel

update: 1/6/2021
Going to try to modify this to actually work properly, by pulling for 
"""


import scrapy
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dateutil import parser

def geturls(ticker):
    # simple file fetcher + formatting
    listimport=pd.read_csv(r"C:\Users\cukel\OneDrive\Documents\PyScripts\hotshot finance type shit\ticker_releasedata\raw\{0}.txt".format(ticker), names=['link'])['link'].tolist()
    return listimport

def getdatetime(dtime):
    return parser.parse(dtime,tzinfos={"EST":-5*3600, "EDT":-4*3600})

class PrSpider(scrapy.Spider):
    
    name='prdriver'
    def __init__(self,ticker):
        self.ticker=ticker
        self.start_urls=geturls(ticker)
    def parse(self, response):
        soupage=BeautifulSoup(response.text,'lxml')
        # get elements with soup
        header=soupage.find('h1', class_='press-release-header__title').text.replace('\n','').replace('  ','')
        timestamp_date=soupage.find('time', class_='timestamp__date').text
        content=soupage.find_all('p')
        fulltext=''
        # pull out the actual article
        for paragraph in content:
            text=paragraph.get_text()
            text=text.replace('\n','').replace('  ','')
            try:
                if text.split()[0].lower()=='about' and len(text.split())<8:
                    break
            except IndexError:
                continue
            fulltext=fulltext+text+' '
        sid=SentimentIntensityAnalyzer()
        ss=sid.polarity_scores(fulltext)
        
        yield {
            'link':response.url,
            'datetime':getdatetime(timestamp_date),
            'fulltext':fulltext,
            'sentiment':ss
            }