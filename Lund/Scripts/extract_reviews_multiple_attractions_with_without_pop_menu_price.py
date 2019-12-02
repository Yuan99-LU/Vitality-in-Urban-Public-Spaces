#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: Volker Strobel
from bs4 import BeautifulSoup
import urllib
from urllib2 import Request, build_opener, HTTPCookieProcessor
from cookielib import LWPCookieJar
import re
import time
import sys
import ssl
import os
import pandas as pd


from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import json



ssl._create_default_https_context = ssl._create_unverified_context

PATH = 'review_output/'

#'https://www.tripadvisor.com/Attraction_Review-g189838-d9750031-Reviews-Lund_University_Main_Building-Lund_Skane_County.html'

if not os.path.exists(PATH):
    os.makedirs(PATH)

def webdriver_start(url):
    driver = webdriver.Chrome('Environment_Variables/chromedriver')
    time.sleep(5)

    return driver


def soup_one_page(driver):
    """
    Helper method, sends HTTP request and returns response payload.
    """
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    return soup

    
def main_one_attraction(URL_LUND, FILE_PATH):
    
    url  = URL_LUND
    driver = webdriver_start(url)
    driver.get(url)
    soup = soup_one_page(driver)
    div = 'script'
    classes = 'application/ld+json'
    data = soup.find(div, {"type": classes})

    data_j =json.loads(data.text)
    
    name = []
    res_url = []
    review_count =[]
    agg_rating_value = []
    price_range = []
    address = []
    post_code = []
    type_category = []
    try:
        name.append(data_j['name'])
    except KeyError:
        name.append(None)
    try:
        res_url.append(data_j['url'])
    except KeyError:
        res_url.append(None)
    try:
        review_count.append(data_j['aggregateRating']['reviewCount'])
    except KeyError:
        review_count.append(None)
    try:
        agg_rating_value.append(data_j['aggregateRating']['ratingValue'])
    except KeyError:
        agg_rating_value.append(None)
    try:
        price_range.append(data_j['priceRange'])
    except KeyError:
        price_range.append(None)
    try:
        address.append(data_j['address']['streetAddress'])
    except KeyError:
        address.append(None)
    try:
        post_code.append(data_j['address']['postalCode'])
    except KeyError:
        post_code.append(None)
    try:
        type_category.append(data_j['@type'])
    except KeyError:
        type_category.append(None)

    DF = pd.DataFrame({"name": name, "url": res_url, "review count": review_count, "aggregating rating value": agg_rating_value,
                      "price range": price_range, "address": address, "postcode": post_code, "category": type_category})

    DF = DF[["name", "url", "review count", "aggregating rating value",
                      "price range", "address", "postcode", "category"]]

    DF.to_csv(FILE_PATH,
                sep=',', encoding="utf-8", index = False,
                header = False, mode = "a")
             
    driver.quit()

    
                
if __name__ == "__main__":
    
    URL_LUND_Group = ['https://www.tripadvisor.com/Restaurant_Review-g189838-d13081859-Reviews-Pinchos-Lund_Skane_County.html',
                      'https://www.tripadvisor.com/Restaurant_Review-g189838-d7104393-Reviews-Viggos_The_Bar-Lund_Skane_County.html',
                      'https://www.tripadvisor.com/Restaurant_Review-g189838-d10513973-Reviews-Wok_Kitchen-Lund_Skane_County.html',
                      'https://www.tripadvisor.com/Restaurant_Review-g189838-d9742916-Reviews-Kinjo_Sushi-Lund_Skane_County.html',
                      'https://www.tripadvisor.com/Restaurant_Review-g189838-d1043214-Reviews-Speedy_Lee_Asian_Foodcourt_AB-Lund_Skane_County.html',]

    for URL_LUND in URL_LUND_Group[0:]:
        CITY_ID = URL_LUND[URL_LUND.find('g189838-')+ 8: URL_LUND.find('-Reviews')]
        print(CITY_ID)
        PLACE = URL_LUND[URL_LUND.find('Reviews-')+ 8: URL_LUND.find('-Lund_Skane_County.html')]
        FILE_PATH = PATH + 'Lund_restaurants' + "_overview180-184.csv"
        if not os.path.exists(FILE_PATH+'s'):
            main_one_attraction(URL_LUND, FILE_PATH)
        else:
            print("file name {} already exsits".format(FILE_PATH))
            print("break due to file exisits")
            break
    print('done')
        
