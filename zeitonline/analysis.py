# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:00:32 2018

@author: elvis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import os

import spacy
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from bs4 import BeautifulSoup
from contractions import CONTRACTION_MAP
import unicodedata

nlp = spacy.load('de_core', parse=True, tag=True, entity=True)
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('german')
stopword_list.remove('no')
stopword_list.remove('not')