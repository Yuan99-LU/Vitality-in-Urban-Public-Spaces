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
    
    #if(more_languages==True):
    #    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[.="More languages"]'))).click()
    #    language_drivers = wait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="more-options"]//label')))
    #else:
    #drivers1= driver.find_elements_by_xpath("//div[contains(@class,'choices is-shown-at-tablet')]")
    language_drivers = driver.find_elements_by_xpath("//label[@for='LanguageFilter_0']")
    #language_drivers = drivers1[0].find_elements_by_xpath("//label[@class='label']")
    print(language_drivers)
    print(len(language_drivers))
    N_all_lang = len(language_drivers)
    #N_all_lang = len(language_drivers)
    select_lang = language_drivers[0].text.split(' ')[0:-1]
    N_select_lang = language_drivers[0].text.split(' ')[-1].strip('()')
    print(N_select_lang)
    language_drivers[0].click()
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
    classes = "hotels-hotel-review-community-content-review-list-parts-SingleReview__reviewContainer--2z_Vq"
    review_paras= soup.find_all("div", {"class": classes})
    #print(review_paras[0:1])
    #print(N)
    #div = 'span'
    #@classes = 'reviews_header_count'
    #total_review_count = int(soup.find(div, {"class": classes}).text[1:-1])
    #print(total_review_count)
    #page_number = (total_review_count-1)//10
    #print(page_number)

    authors = []
    rating_scores = []
    rating_dates = []
    titles = []
    #places = []
    review_texts= []
    response_titles = []
    response_dates =[]
    response_texts = []
    stay_dates =[]
    N_reviews = len(review_paras)
    language = [select_lang]*N_reviews
    reviews_per_language = [N_select_lang]*N_reviews

    print(N_reviews)
        
    for review_para in review_paras[0:]:
        
        soup2 = review_para

        ################################################################################
        div = 'a'
        classes ='ui_link social-member-MemberEventOnObjectBlock__member--21vv3'
        #author_contributions, N = get_one_item(soup2, div, classes)
        try:
            author = soup2.find(div, {"class": classes})
            if(author is not None):
                authors.append(author.text)
            else:
                authors.append('')
        except AttributeError as e:
            print(e)
            authors.append('')
        #print(author.text)
        
        ################################################################################
            
        ################################################################################
        div = 'span'
        classes = 'ui_bubble_rating bubble'
        rating_score = soup2.find(div, {"class": re.compile(classes)})
        if(rating_score is not None):
            rating_scores.append(rating_score['class'][1][-2:-1])
        else:
            rating_scores.append('')
        #print(rating_score['class'][1][-2:-1])
        ################################################################################

        ################################################################################    
        div = 'span'
        classes = 'social-member-MemberEventOnObjectBlock__item--27qCT'
        rating_date = soup2.find(div, {"class": classes})
        if(rating_date is not None):
            rating_dates.append(rating_date.text)
        else:
            rating_dates.append('')
        #print(rating_date.text)
        ################################################################################
        
        ################################################################################
        div = 'a'
        classes = 'hotels-hotel-review-community-content-review-list-parts-ReviewTitle__reviewTitleText--2vGeO'
        title = soup2.find(div, {"class": classes})
        if(title is not None):
            titles.append(title.text)
        else:
            titles.append('')
        #print(title.text)
        ################################################################################

        ################################################################################
        div = 'q'
        classes = 'hotels-hotel-review-community-content-review-list-parts-ExpandableReview__reviewText--1OjOL'
        review_text = soup2.find(div, {"class": classes})
        if(review_text is not None):
            review_texts.append(review_text.text)
        else:
            review_texts.append('')
        #print(review_text.text)
        ################################################################################

        ################################################################################
        try:
            div = 'div'
            classes = 'hotels-hotel-review-community-content-review-list-parts-OwnerResponse__header--1qaPT'
            response_title = soup2.find(div, {"class": classes})
            if(response_title is not None):
                response_titles.append(response_title.text)
            else:
                response_titles.append('')
            #print(response_title.text)
        except AttributeError as e:
            print(e)
            response_titles.append('')
        ################################################################################

        ################################################################################
        try:
            div = 'div'
            classes = 'hotels-hotel-review-community-content-review-list-parts-OwnerResponse__responseDate--1LWhd'
            response_date = soup2.find(div, {"class": classes})
            if(response_date is not None):
                response_dates.append(response_date.text)
            else:
                response_dates.append('')
            #print(response_date.text)
        except AttributeError as e:
            print(e)
            response_dates.append('')
        
        ################################################################################

        ################################################################################
        try:
            div = 'span'
            classes = 'hotels-hotel-review-community-content-review-list-parts-OwnerResponse__reviewText--1cPU0'
            response_text = soup2.find(div, {"class": classes})
            if(response_text is not None):
                response_texts.append(response_text.text)
            else:
                response_texts.append('')
            #print(response_text.text)
        except AttributeError as e:
            print(e)
            response_texts.append('')
        ################################################################################

        ################################################################################
        try:
            div = 'span'
            classes = 'hotels-review-list-parts-EventDate__bold--2phZA'
            stay_date = soup2.find(div, {"class": classes})
            if(stay_date is not None):
                stay_dates.append(stay_date.parent.text)
            else:
                stay_dates.append('')
                #print(stay_date.text)
        except AttributeError as e:
            print(e)
            stay_dates.append('')
        ################################################################################
    print(len(authors))
    print(len(rating_dates))
    print(len(rating_scores))
    print(len(titles))
    print(len(review_texts))
    print(len(response_titles))
    print(len(response_dates))
    print(len(response_texts))
    print(len(stay_dates))
    print(len(language))
    print(len(reviews_per_language))
    
    DF = pd.DataFrame({"author": authors, "rating_date": rating_dates, "rating_score": rating_scores,
                          "title":titles, "review_text": review_texts, "response_title": response_titles, "response_date": response_dates,
                           "response_text":response_texts, "stay_date":stay_dates, 'language':language, "reviews_per_language":reviews_per_language
                  })
    success = True

    return DF, success, N_reviews

def write_to_csv(DF, FILE_PATH):
        
    DF = DF[["author", "rating_date", "rating_score","title", "review_text", "response_title", "response_date",
                           "response_text", "stay_date", 'language', "reviews_per_language"]]
    DF.to_csv(FILE_PATH,
                sep=',', encoding="utf-8", index = False,
                header = False, mode = "a")
    #return DF

    
def main_one_attraction(URL_LUND, FILE_PATH):
    
    url  = URL_LUND
    driver = webdriver_start(url)
    driver.get(url)
    i_initial = 1
    #driver, N_all_lang, select_lang, N_select_lang = select_language(driver, i_initial)
    #print(driver, N_all_lang, select_lang, N_select_lang)
    print('initial page is loaed, starting downloading the data -------------')
    for i in range(0, 1):
        
        url  = URL_LUND
        driver.get(url)
        driver, N_all_lang, select_lang, N_select_lang = select_language(driver, i)
        time.sleep(10)

        soup = soup_one_page(driver)
        DF, success, N_reviews = get_results(soup, select_lang, N_select_lang)
        
        write_to_csv(DF, FILE_PATH)

        if(N_reviews >5):
            print("----------more than 10 reviews, break to check problems------------------")
            break
        N = 0
        while(N_reviews==5):
            N+=1
            try:
                print("page number is {}".format(N))
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
    N_hotel = 29
    for URL_LUND in URL_LUND_Group[N_hotel+1:]:
        N_hotel +=1
        print("the {}th hotel is in processing -----".format(N_hotel))
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
        
