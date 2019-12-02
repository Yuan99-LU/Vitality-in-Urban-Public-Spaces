#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: Volker Strobel
from bs4 import BeautifulSoup
import urllib
from urllib2 import URLError, Request, build_opener, HTTPCookieProcessor, ProxyHandler
from cookielib import LWPCookieJar
import re
import time
import sys
import ssl

import pandas as pd
import random
import socket
from httplib import BadStatusLine, HTTPException
#socket.setdefaulttimeout(3)

ssl._create_default_https_context = ssl._create_unverified_context

#-------------------------------------------------------------------------------
SEARCH_NAME = '"city vitality"'
START_YEAR = 1959
END_YEAR = 1959
INTERUPT = 1
#-----------------------------------------------------------------------------

order = 'f46e1c2a81076398aee641141f337d0b'
apiUrl = 'https://free-socks.in/api/v1/get_proxy?apikey=3OSIE19UDGBRICSQQ6JQ4X9E1Q8PILWB'
#apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=f46e1c2a81076398aee641141f337d0b&sep=3"

#134.209.22.245:3128
#95.86.48.148:33304
def get_proxy_ip():
    proxyip = '95.86.48.148:33304'
    return proxyip

def get_proxy_ip_t():
    with open("proxy_list.txt") as f:
        content = f.readlines()
    content =[x.strip() for x in content]
    print(len(content))
    sr = random.SystemRandom()
    proxyip_gaoni =sr.choice(content)
    proxyip=proxyip_gaoni.split(" ")[0]
    #proxyip = content
    print(proxyip)
    return proxyip

#ip = get_proxy_ip()
#print()

def get_proxy_ip_data5u():
    print("it is getting proxyip---")
    res = urllib.urlopen(apiUrl).read().strip("\n")
    time.sleep(2)
    ips = res.split("\n")
    sr = random.SystemRandom()
    proxyip_gaoni =sr.choice(ips)
    proxyip=proxyip_gaoni.split(",")[0]
    
    print(proxyip)
    
    return proxyip

def soup_one_page(search_term, start_date, end_date, page_number, proxyip, cookies):
    """
    Helper method, sends HTTP request and returns response payload.
    """
    N=0;
    while(True):
        N+=1
        if(N>=2):
            print("while loop in soup_one_page is %d" %N)
        try:
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36 Firefox/43.0 Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101'
            #query_params = {'lr': language, 'start':page_number, 'q' : search_term, 'as_ylo' : start_date, 'as_yhi' : end_date}
            query_params = {'start':page_number, 'q' : search_term, 'as_ylo' : start_date, 'as_yhi' : end_date}
            url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + urllib.urlencode(query_params)
            print url

            proxy={"https": proxyip}
            proxy_support = ProxyHandler(proxy)

            opener = build_opener(proxy_support, HTTPCookieProcessor(cookies))
            request = Request(url=url, headers={'User-Agent': user_agent})
            handler = opener.open(request)
            
            html = handler.read() 
            soup = BeautifulSoup(html, 'html.parser')

            break

        except URLError as e:
            print("URLError----")
            print(e.reason)
            proxyip = get_proxy_ip()
            continue

        except HTTPException:
            print("HTTPException----")
            proxyip = get_proxy_ip()
            continue

        except BadStatusLine:
            print("BadStatusLine----")
            proxyip = get_proxy_ip()
            continue

        except socket.timeout as e:
            print("Socket Timeout Error")
            proxyip = get_proxy_ip()
            continue

        except socket.error:
            print("Socket SocketError")
            proxyip = get_proxy_ip()
            continue
    
    return soup, proxyip


def get_total_number(soup, i):
    print("it is finding total number of papers/books---------------------------")
    div_results = soup.find("div", {"id": "gs_ab_md"}) # find line 'About x results (y sec)
    #print div_results[]
    if div_results !=[] and div_results !=None:
        res = re.findall(r'(\d+),?(\d+)?,?(\d+)?\s', div_results.text)
        if(len(res)>=2):
            num = int(''.join(res[i]))
        elif(len(res)==1):
            num = int(''.join(res[0]))
        else:
            print("res is equal 0")
            num = 0
            print(res)
        
        print(num)
        success = True
    else:
        print("page 1 is empty, try it again")
        num = 0
        success = False
    return num, success


def get_results(soup, date, i):
    total_number, success = get_total_number(soup, i)
    print("it is finding title----------------------------------------------------")
    div_results = soup.find_all("h3", {"class": "gs_rt"})
    #print(div_results)
    title_info=[]
    num_info=[]
    date_info=[]
    #div_results =[]
    #print div_results
    
    if div_results !=[]:
        for div_result in div_results:
            title_info.append(div_result.text)
            num_info.append(total_number)
            date_info.append(date)

        #print("it is finding authors------------------------------------------------")
        author_info=[]
        div_results = soup.find_all("div", {"class": "gs_a"})
        for div_result in div_results:
            author_info.append(div_result.text)

        #print("it is finding text----------------------------------------------------")
        text_info=[]
        div_results = soup.find_all("div", {"class": "gs_rs"})
        for div_result in div_results:
            text_info.append(div_result.text)
        if(len(text_info)!=len(title_info)):
            text_info=[None]*len(title_info)
            
        print("it is finding citation----------------------------------------------------")
        div_results = soup.find_all("div", {"class": "gs_fl"})
        cite_info=[]
        for div_result in div_results:
            if 'gs_ggs' not in div_result.attrs['class']:
                cite_info.append(div_result.text)

        DF = pd.DataFrame({"date": date_info, "num": num_info, "title": title_info,
                           "author": author_info, "text": text_info, "cite_by": cite_info
                  })
        success = True
        
    else:
        print "no content has found in this page, try search this page again"
        DF=[]
        success = False

    return DF, success, total_number



def write_to_csv(DF):
    DF = DF[["date","num", "title", "author","text","cite_by"]]
    DF.to_csv("./output_vitality/"+SEARCH_NAME+".csv",
                sep=',', encoding="utf-8", index = False,
                header = False, mode = "a")
    return DF


def get_range(search_term, start_date, end_date, proxyip):
#################################################for start page 1################################
    for date in range(start_date, end_date + 1):
        print("current year in search is %d" %date)
        cookies = LWPCookieJar('./cookies')
        try:
            cookies.load()
        except IOError:
            pass
           
        page_number =10*(INTERUPT - 1)
        print("start page number is %d" %page_number)
        soup, proxyip = soup_one_page(search_term, date, date, page_number, proxyip, cookies)
        if(INTERUPT!=1):
            DF, success, total_number = get_results(soup, date, i=1)
        elif(INTERUPT==1):
            DF, success, total_number = get_results(soup, date, i=0)
       
        while(success==False):
            print("enter the firt while loop due to first page is empty")
            proxyip = get_proxy_ip()
            soup, proxyip = soup_one_page(search_term, date, date, page_number, proxyip, cookies)
            time.sleep(5)
            if(INTERUPT!=1):
                DF, success, total_number = get_results(soup, date, i=1)
            elif(INTERUPT==1):
                DF, success, total_number = get_results(soup, date, i=0)
            if(success):
                break
            
              
        print("total number is %d" %total_number)
        if total_number !=0:
            if(INTERUPT!=1):
                print("INTERUPT from page %d" %INTERUPT)
                #print("temporariliy use to avoid doulbe first page and continue write to CSV")
            elif(INTERUPT==1):
                print("No INTERUPT, start from page %d" %INTERUPT)
                if(success):
                    write_to_csv(DF)
            if(total_number > 10):
                page_number = 10*((total_number-1) // 10)
                soup, proxyip = soup_one_page(search_term, date, date, page_number, proxyip, cookies)
                DF, success, total_number = get_results(soup, date, i=1)
        else:
            print("no publication has found for year %d" %date)
####################################################################################################              
#################################################for all pages after page 1#########################
        page_numbers = (total_number-1) // 10
        
        if(page_numbers > 100):
            page_numbers=99
        M=0

        for j in range(INTERUPT, page_numbers + 1):
            
            print("page number %d is processing in total %d pages" %(j,page_numbers))
            page_number =j*10
            #print("page number is %d" %page_number)
            soup, proxyip = soup_one_page(search_term, date, date, page_number, proxyip, cookies)
            time.sleep(1)
          
            DF, success, total_number = get_results(soup, date, i=1)
            if(success):
                if(page_number>total_number):
                    print("it is breaking due to page number %d is larger than total number %d" %(page_number, total_number))
                    break

            N = 0
            while(success==False):
                print("enter the second while loop due to page %d is empty" %j)
                proxyip=get_proxy_ip()
                soup, proxyip = soup_one_page(search_term, date, date, page_number, proxyip, cookies)
                time.sleep(1)
                DF, success, total_number = get_results(soup, date, i=1)
                N+=1
                
                if(success):
                    break
                print("N in while loop is %d" %N)
                if(j>=95):
                     if (N==2):
                        M+=1;
                        break
                if(N==100):
                    M+=1;
                    print("break to next year due to N= %d is large than 100" % N)
                    break
                    
            #page_numbers = (total_number-1) // 10
                
            if(M==2):
                print("break the whole loop due to M= %d is large than 100" % M)
                break
            #page_numbers = (total_number-1) // 10
            if(success):
            #page_numbers = (total_number-1) // 10
                write_to_csv(DF)
                
    #cookies.save()
#################################################################################################### 
    return soup
####################################################################################################
              


if __name__ == "__main__":

    try:
        search_term = SEARCH_NAME
        start_date = START_YEAR
        end_date = END_YEAR
        #language = 'lang_zh-CN'
        #language = 'lang_en'

        proxyip = get_proxy_ip()
        html = get_range(search_term, start_date, end_date, proxyip)
        
    except Exception as e:
        print("main Exception in main funciton")
        print(e)
        
    finally:
        print("done")
        #cookies.save()


