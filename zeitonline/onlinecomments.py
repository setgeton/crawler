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

    
from warnings import warn

warn("Warning Simulation")

usernames = []
cmnumbers = []
text = []
overlayurls =[]

pages = [str(i) for i in range(1,2)] #which pages to crawl
      
start_time = time()
requests = 0

headers = {"Accept-Language": "en-US, en;q=0.5"}

for page in pages:

    sleep(randint(1,11))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)


    url='https://www.zeit.de/politik/ausland/2018-07/fluechtlinge-horst-seehofer-kabul-abschiebung-selbstmord?page='+page+'#comments'
    response=get(url, headers = headers)
    
    
    page_html = BeautifulSoup(response.text, 'html.parser')
    
    # Select all the 50 movie containers from a single page
    name_containers = page_html.find_all('div', class_="comment-meta__name")
    cmnumber_containers = page_html.find_all('a', class_="comment-meta__date")
    text_containers = page_html.find_all('div', class_="comment__body")
    #overlayurl_container = page_html.find_all('div', class_="comment-overlay js-load-comment-replies")

    #print(type(name_containers))
    #print(len(name_containers))

   
    for container in name_containers:
            #scrape username
        name = container.a.text
        usernames.append(name)
    
    for container in cmnumber_containers:
            #scrape commentnumber
        number = container.text
        cmnumbers.append(number)
    
    for container in text_containers:
            #scrape textbody
        textfrag = container.text
        text.append(textfrag)
        
        
  #  for container in overlayurl_container:
  #      #overlay url to be extracted later
  #     ourl=container.find('div')['data-url']
  #     overlayurls.append(ourl)

        
zeitcomments = pd.DataFrame({'username': usernames,
                              '#num': cmnumbers,
                              'text': text})
print(zeitcomments.info())
zeitcomments.head(30)
       