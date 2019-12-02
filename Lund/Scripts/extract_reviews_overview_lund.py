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
    
    URL_LUND_Group = ['https://www.tripadvisor.com/Hotel_Review-g189838-d5272660-Reviews-Radisson_Blu_Hotel_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d8144468-Reviews-Best_Western_Plus_Hotell_Nordic_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d233622-Reviews-Grand_Hotel_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d3936828-Reviews-Elite_Hotel_Ideon-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d1488628-Reviews-Forenom_Aparthotel_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d3216656-Reviews-The_More_Hotel_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d1201469-Reviews-Hotell_Oskar-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d2439785-Reviews-MillasVilla-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d233078-Reviews-Clarion_Collection_Hotel_Planetstaden-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d241984-Reviews-Hotel_Concordia-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d250818-Reviews-Hotel_Lundia-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d254946-Reviews-Scandic_Hotel_Star_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d231807-Reviews-Good_Morning_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d2410917-Reviews-Hotel_Finn-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d1045316-Reviews-Lilla_Hotellet-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d10228542-Reviews-Hotel_Bishops_Arms-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d227500-Reviews-Hotel_Djingis_Khan-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d3395287-Reviews-Magles_Smiley_Inn-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d2542935-Reviews-Hobykrok_B_B-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d9755061-Reviews-Explorers_Club-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d3838987-Reviews-Brunius_Bed_and_Breakfast-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d233077-Reviews-Hotel_Ideon_Gasteri-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d2067323-Reviews-No_1_Guest_House-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d1229129-Reviews-Hotell_Ahlstrom-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d3453510-Reviews-Garden_House_and_Rooms-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d285137-Reviews-Hotell_Sparta-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d6211189-Reviews-Hotell_Overliggaren-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d12251525-Reviews-Villa_Pedell-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d5825219-Reviews-Winstrup_Hostel-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d10355542-Reviews-Fenix_Inn-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d15638593-Reviews-Villa_Vega_Apartments-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d15467221-Reviews-Villa_Weibull-Lund_Skane_County.html',
'https://www.tripadvisor.com/Hotel_Review-g189838-d6850020-Reviews-Villa_Nova_Apartments-Lund_Skane_County.html',]

    for URL_LUND in URL_LUND_Group[0:]:
        CITY_ID = URL_LUND[URL_LUND.find('g189838-')+ 8: URL_LUND.find('-Reviews')]
        print(CITY_ID)
        PLACE = URL_LUND[URL_LUND.find('Reviews-')+ 8: URL_LUND.find('-Lund_Skane_County.html')]
        FILE_PATH = PATH + 'Lund_to_do_things' + "_overview.csv"
        if not os.path.exists(FILE_PATH+'s'):
            main_one_attraction(URL_LUND, FILE_PATH)
        else:
            print("file name {} already exsits".format(FILE_PATH))
            print("break due to file exisits")
            break
    print('done')
        
