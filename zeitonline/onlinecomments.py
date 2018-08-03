# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:53:25 2018

@author: setgeton
"""


from requests import get
from bs4 import BeautifulSoup

from time import sleep
from time import time
from random import randint


from IPython.core.display import clear_output

import re 
    
from warnings import warn

warn("Warning Simulation")

articleurl='https://www.zeit.de/2018/32/demokratie-postdemokratie-mittelschicht-modernisierungsverlierer'
response=get(articleurl)
page_html = BeautifulSoup(response.text, 'html.parser')

articleparas=[]
headline=[]
summary=[]

para_containers = page_html.find_all('p', class_="paragraph article__item")
summary_container = page_html.find('div', class_="summary")
headline_container = page_html.find('span', class_="article-heading__title")

for container in para_containers:
            #scrape paragraphs of the article
        para = container.text
        para = re.sub('\n', ' ', para)
        para = re.sub(';', ',', para)
        articleparas.append(para)

summary=summary_container.text
headline=headline_container.text


cmsection = page_html.find('div', class_="comment-section__item").small.text[-5:]
if type(cmsection) is None:
    cmsection="      1"

maxcmpage=re.sub("[^0-9]", "", cmsection)






usernames = []
cmnumbers = []
text = []
overlayurls =[]


pages = [str(i) for i in range(1,int(maxcmpage)+1)] #which pages to crawl
#pages = [str(i) for i in range(1,3)]  #only first 2 pages of comments

     
start_time = time()
requests = 0

#headers = {"Accept-Language": "en-US, en;q=0.5"}





for page in pages:

    sleep(randint(1,3))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)


    url=articleurl+'?page='+page+'#comments'
    response=get(url) #  get(url, headers = headers)
    
    
    page_html = BeautifulSoup(response.text, 'html.parser')
    
    # Select all the 50 movie containers from a single page
    name_containers = page_html.find_all('div', class_="comment-meta__name")
    cmnumber_containers = page_html.find_all('a', class_="comment-meta__date")
    text_containers = page_html.find_all('div', class_="comment__body")
    overlayurl_container = page_html.find_all('div', class_="comment__container js-comment-loader")

    #print(type(name_containers))
    #print(len(name_containers))

   
    for container in name_containers:
            #scrape username
        name = container.a.text
        name = re.sub(';', ',', name)
        usernames.append(name)
    
    for container in cmnumber_containers:
            #scrape commentnumber
        number = container.text[18:26]
        cmnumbers.append(number)
    
    for container in text_containers:
            #scrape textbody
        textfrag = container.text[1:-1]
        textfrag = re.sub('\n', ' ', textfrag)
        textfrag = re.sub(';', ',', textfrag)
        text.append(textfrag)
        
        
    for container in overlayurl_container:
       #overlay url to be extracted later
       ourl=container.find('a')['data-url']
       overlayurls.append(ourl)

for url in overlayurls:
    
    sleep(randint(1,2))
    
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    
    response=get(url) #  get(url, headers = headers)
    page_html = BeautifulSoup(response.text, 'html.parser')
    name_containers = page_html.find_all('div', class_="comment-meta__name")
    cmnumber_containers = page_html.find_all('a', class_="comment-meta__date")
    text_containers = page_html.find_all('div', class_="comment__body")
    
    for container in name_containers:
            #scrape username
        name = container.a.text
        name = re.sub(';', ',', name)
        usernames.append(name)
    
    for container in cmnumber_containers:
            #scrape commentnumber
        number = container.text[18:26]
        cmnumbers.append(number)
    
    for container in text_containers:
            #scrape textbody
        textfrag = container.text[1:-1]
        textfrag = re.sub('\n', ' ', textfrag)
        textfrag = re.sub(';', ',', textfrag)
        text.append(textfrag)
    
    

import pandas as pd
import numpy as np

cmind=[int(i) for i in range(0,len(cmnumbers))]
primcmnum=np.zeros((len(cmnumbers),1)).tolist()
subcmnum=np.zeros((len(cmnumbers),1)).tolist()

for ind in cmind:
    cmnumbers[ind] = re.sub('\xa0', '', cmnumbers[ind])
    cmnumbers[ind] = re.sub("[^0-9^.]+", "", cmnumbers[ind])
    tempnumlist=[]
    tempnumlist=re.split(r"[.]", cmnumbers[ind])    
    primcmnum[ind]=int(tempnumlist[0])
    if len(tempnumlist) is 1:
            subcmnum[ind]=0
    if len(tempnumlist) is 2:
            subcmnum[ind]=int(tempnumlist[1])

  
zeitcomments = pd.DataFrame({'username': usernames,
                              'primcmnum': primcmnum,
                              'subcmnum': subcmnum,
                              'text': text})

articleb=[headline,summary]+articleparas
articlebody = pd.DataFrame({'text': articleb})    

zeitcomments.to_csv('zeitcomments.csv', sep=';', encoding='utf-8-sig')  
articlebody.to_csv('article.csv', sep=';', encoding='utf-8-sig')    
    
print(zeitcomments.info())
zeitcomments.head(10)

print(zeitcomments['text'][10])
