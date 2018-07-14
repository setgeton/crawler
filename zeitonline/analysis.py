# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:00:32 2018

@author: elvis
"""

import spacy
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re

from nonwords_de import nonwordslist_de

article = pd.read_csv("article.csv",delimiter=';')
arttext=np.asarray(article['text'].astype('str')).ravel().tolist()
arttext=' '.join(arttext)

arttext=re.sub('/sq', ' ', arttext)
arttext=re.sub('/spt', ' ', arttext)
arttext=re.sub('[^a-z^A-Z^ä^ö^ü^ß^Ä^Ö^Ü]+', ' ', arttext)
articletokens = [t for t in arttext.split()]


data = pd.read_csv("zeitcomments.csv",delimiter=';')
textlist=np.asarray(data['text'].astype('str')).ravel().tolist()
numofcm=len(textlist)
endlostext=' '.join(textlist)
endlostext=re.sub('/sq', ' ', endlostext)
endlostext=re.sub('/spt', ' ', endlostext)
endlostext=re.sub('[^a-z^A-Z^ä^ö^ü^ß^Ä^Ö^Ü]+', ' ', endlostext)
tokens = [t for t in endlostext.split()]
freq = nltk.FreqDist(tokens)
freqlist=[]
for key,val in freq.items():
   if numofcm * 0.01<val:
       if not str(key) in nonwordslist_de:
         if not str(key) in articletokens:  
             print (str(key) + ':' + str(val))
             freqlist.append(str(key))
        
#nlp = spacy.load('de', parse=True, tag=True, entity=True)
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)
#tokenizer = ToktokTokenizer()
#doc = nlp(textlist[0])
#print(doc.text)
#for token in doc:
 #   print(token.text, token.pos_, token.dep_)

