# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 23:53:00 2021

@author: Luke
"""

from selenium import webdriver #import
try:
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless=True
    brower = webdriver.Firefox(options=fireFoxOptions)

    brower.get('https://pythonbasics.org')
    print(brower.page_source)
finally:
    try:
        brower.close()
    except:
        pass