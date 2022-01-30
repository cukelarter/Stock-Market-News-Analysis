# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 01:51:13 2022

@author: Luke
"""

def pr_fullpull(ticker, export=True):
    # gets all press releases of input ticker and outputs to raw data file
    # stored in hotshot finance type shit\ticker_releasedata\raw
    # development was done under "News Lagtime Exploitation"
    # TO DO:
        # implement headless browsing
    from selenium import webdriver #import
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    import numpy as np
    import time
    # start the driver
    browser=webdriver.Edge("C:/Users/Luke/Downloads/edgedriver_win32/msedgedriver.exe")
    # generate and retreive url
    url='https://www.nasdaq.com/market-activity/stocks/{}/press-releases'.format(ticker.lower())
    browser.get(url)
    out_hrefs=[]
    page=1
    maxpages=2
    # apply methods to get desired info from elements
    while True:
        try:
            # end if it its too far along
            if page==maxpages:
                break
            # take a break for a sec
            time.sleep(0.5)
            # go to specific start point 
            browser.execute_script("window.scrollTo(0,330)")
            # find the required href elements
            a_eles = browser.find_elements_by_xpath("//a[@class='quote-press-release__link']")
            browser.execute_script("arguments[0].scrollIntoView();", a_eles[0])
            # then go up a little, basically the sweet spot (in theory)
            browser.execute_script("window.scrollBy(0,-100)")
            # append them to list
            for ii in range(len(a_eles)):
                # try block 1
                # gets around stale exception errors (in theory)
                unclicked0=True
                tries0=0
                while unclicked0 and tries0<10:
                    try:
                        href = a_eles[ii].get_attribute("href")
                        out_hrefs.append(href)
                        unclicked0=False
                    except:
                        tries0+=1
                        continue
            # get max page, check to see if we're past it
            # only do on first page
            if page==1:
                allpages=browser.find_elements_by_xpath("//button[@class='pagination__page']")
                #for npage in allpages:
                    #if int(npage.text)>maxpages:
                        #maxpages=int(npage.text)
                maxpages=int(allpages[-1].text)
            # if we're still under the max pages
            if page<maxpages:
                # try block 2
                unclicked1=True
                tries1=0
                while unclicked1 and tries1<10:
                    try:
                        # get the button
                        nextbutton=browser.find_element(By.CLASS_NAME,'pagination__next')
                        browser.execute_script("arguments[0].scrollIntoView();", nextbutton)
                        # then go up a little
                        browser.execute_script("window.scrollBy(0,-100)")
                        # make sure next arrow is clickable
                        WebDriverWait(browser, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME,'pagination__next')))
                        # click the next arrow
                        nextbutton.click()
                        page+=1
                        unclicked1=False
                    except:
                        tries1+=1
                        continue
            
        except IndexError:
            # no press releases on the site
            out_hrefs.append([ticker,np.nan])
            break
    browser.close()
    
    # export to external list for this ticker
    if export:
        try:
            file_path='C:/Users/Luke/OneDrive/Documents/PyScripts/hotshot finance type shit/ticker_releasedata/raw/%s.txt' % ticker
        
            file=open(file_path, 'w')
            for href in out_hrefs:
                file.write(href)
                file.write('\n')
            file.close()
        except TypeError: # empty page
            print('failed on: '+str(ticker))
#%% Loop for all tickers

import pandas as pd

# retreive health.csv, which contains all symbols, names, and recent statistics of all NASDAQ healthcare stocks
# retreived from https://www.nasdaq.com/market-activity/stocks/screener

df = pd.read_csv('C:/Users/Luke/OneDrive/Documents/PyScripts/hotshot finance type shit/health.csv')
tickers=list(df['Symbol'])
failtick=191 # most recent failure, only have to run once so
# need to fix the need to scroll
for ticker_ii in range(failtick,len(tickers)):
    pr_fullpull(tickers[ticker_ii], export=True)

