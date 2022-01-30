# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 03:29:52 2022

@author: cukel

This should be the file that actually calls scrapy
on each ticker to output results
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from prdriver import PrSpider,geturls,getdatetime
ticker='ABUS'

s = get_project_settings()
s['FEED_FORMAT']='csv'
s['FEED_URI']='tester_{0}'.format(ticker)
process = CrawlerProcess(settings={
    'FEED_FORMAT':'json',
    'FEED_URI': 'results.json'
    })

process.crawl('prdriver',ticker=ticker)
process.start()