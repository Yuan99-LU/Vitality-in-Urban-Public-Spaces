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


cookies = LWPCookieJar('./cookies')
try:
    cookies.load()
except IOError:
    pass

ssl._create_default_https_context = ssl._create_unverified_context

PATH = 'review_output/'

#'https://www.tripadvisor.com/Attraction_Review-g189838-d9750031-Reviews-Lund_University_Main_Building-Lund_Skane_County.html'

if not os.path.exists(PATH):
    os.makedirs(PATH)

def webdriver_start(url):
    driver = webdriver.Chrome('Environment_Variables/chromedriver')
    time.sleep(5)

    return driver

def select_language(driver,i):
    try:
        print(driver.find_element_by_xpath('//span[.="More languages"]'))
        more_languages = True
        print("there is a 'more languages' option")
    except NoSuchElementException as e:
        more_languages = False
        print e
    
    if(more_languages==True):
        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[.="More languages"]'))).click()
        language_drivers = wait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="more-options"]//label')))
    else:
        drivers1= driver.find_elements_by_xpath("//div[contains(@class,'choices is-shown-at-tablet')]")
        language_drivers = drivers1[0].find_elements_by_xpath(".//label[@class='label']")
    
    print(len(language_drivers))
    N_all_lang = len(language_drivers)
    select_lang = language_drivers[i].text.split(' ')[0:-1]
    N_select_lang = language_drivers[i].text.split(' ')[-1].strip('()')
    language_drivers[i].click()
    return driver, N_all_lang, select_lang, N_select_lang

def soup_one_page(driver):
    """
    Helper method, sends HTTP request and returns response payload.
    """
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def get_one_item(soup, div, classes):
    N = 0
    contents = []
    div_results = soup.find_all(div, {"class": classes})
    for div_result in div_results:
        N+=1
        #print('%s----------title number %d is' %(classes, N))
        #print(div_result.text)
        contents.append(div_result.text)
    return contents, N

def get_results(soup, select_lang, N_select_lang):
    print("it is finding title----------------------------------------------------")
    
    div = 'div'
    classes = "prw_rup prw_reviews_review_resp"
    review_paras= soup.find_all("div", {"class": classes})
    #print(review_paras[0:1])
    #print(N)
    div = 'span'
    classes = 'reviews_header_count'
    total_review_count = int(soup.find(div, {"class": classes}).text[1:-1])
    print(total_review_count)
    #page_number = (total_review_count-1)//10
    #print(page_number)

    author_contributions = []
    author_votes = []
    rating_scores = []
    rating_dates = []
    titles = []
    places = []
    review_texts= []
    N_reviews = len(review_paras)
    language = [select_lang]*N_reviews
    reviews_per_language = [N_select_lang]*N_reviews
        
    for review_para in review_paras[0:]:
        soup2 = review_para
        div = 'span'
        classes ='ui_icon pencil-paper'
        #author_contributions, N = get_one_item(soup2, div, classes)
        try:
            author_contribution = soup2.find(div, {"class": classes}).findNext('span')
            if(author_contribution is not None):
                author_contributions.append(author_contribution.text)
            else:
                author_contributions.append('')
        except AttributeError as e:
            print(e)
            author_contributions.append('')
        #print(author_contribution)

        div = 'span'
        classes ='ui_icon thumbs-up-fill'
        try:
            author_vote = soup2.find(div, {"class": classes}).findNext('span')
            if(author_vote is not None):
                author_votes.append(author_vote.text)
            else:
                author_votes.append('')
        except AttributeError as e:
            print(e)
            author_votes.append('')
        #print(author_vote)
        

        div = 'span'
        classes = 'ui_bubble_rating bubble'
        rating_score = soup2.find(div, {"class": re.compile(classes)})
        if(rating_score is not None):
            rating_scores.append(rating_score['class'][1][-2:-1])
        else:
            rating_scores.append('')
        #print(rating_score)
        
        div = 'span'
        classes = 'noQuotes'
        title = soup2.find(div, {"class": classes})
        if(title is not None):
            titles.append(title.text)
        else:
            titles.append('')
        #print(title)

        div = 'div'
        classes = 'userLoc'
        place = soup2.find(div, {"class": classes})
        if(place is not None):
            places.append(place.text)
        else:
            places.append('')
        #print(place)
        
        div = 'p'
        classes = 'partial_entry'
        review_text = soup2.find(div, {"class": classes})
        if(review_text is not None):
            review_texts.append(review_text.text)
        else:
            review_texts.append('')
        #print(review_text)

        div = 'span'
        classes = 'ratingDate'
        rating_date = soup2.find(div, {"class": classes})
        if(rating_date is not None):
            rating_dates.append(rating_date.text[9:])
        else:
            rating_dates.append('')

    DF = pd.DataFrame({"author_contributions": author_contributions, "author_votes": author_votes, "rating_score": rating_scores,
                          "rating_date":rating_dates, "title": titles, "place": places, "review_text": review_texts,
                           "language":language, "reviews_per_language":reviews_per_language
                  })
    success = True

    return DF, success, N_reviews

def write_to_csv(DF, FILE_PATH):
        
    DF = DF[["language", "reviews_per_language", "author_contributions","author_votes", "rating_score","rating_date","title", "place", "review_text"]]
    DF.to_csv(FILE_PATH,
                sep=',', encoding="utf-8", index = False,
                header = False, mode = "a")
    #return DF

    
def main_one_attraction(URL_LUND, FILE_PATH):
    
    url  = URL_LUND
    driver = webdriver_start(url)
    driver.get(url)
    i_initial = 1
    driver, N_all_lang, select_lang, N_select_lang = select_language(driver, i_initial)
    #print(driver, N_all_lang, select_lang, N_select_lang)
    print('initial page is loaed, starting downloading the data -------------')
    for i in range(1, int(N_all_lang)):
        url  = URL_LUND
        driver.get(url)
        driver, N_all_lang, select_lang, N_select_lang = select_language(driver, i)
        time.sleep(10)

        soup = soup_one_page(driver)
        DF, success, N_reviews = get_results(soup, select_lang, N_select_lang)
        
        write_to_csv(DF, FILE_PATH)

        if(N_reviews >10):
            print("----------more than 10 reviews, break to check problems------------------")
            break

        while(N_reviews==10):
            try:
                next_pages = wait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH,"//a[.='Next']")))
                #print(next_pages)
                next_pages[0].click()
                time.sleep(10)
                soup = soup_one_page(driver)
                DF, success, _ = get_results(soup, select_lang, N_select_lang)

                write_to_csv(DF, FILE_PATH)
                   
            except WebDriverException as e:
                print(e)
                break
            
    driver.quit()

    #return error


    
                
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
        FILE_PATH = PATH + PLACE + '-ID-' + CITY_ID + ".csv"
        if not os.path.exists(FILE_PATH):
            main_one_attraction(URL_LUND, FILE_PATH)
        else:
            print("file name {} already exsits".format(FILE_PATH))
            print("break due to file exisits")
            break
    print('done')
        
