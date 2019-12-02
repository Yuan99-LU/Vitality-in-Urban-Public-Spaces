import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as mpl
from nltk.tag import pos_tag
from googletrans import Translator
#import matplotlib.use

mpl.style.use('ggplot')
mpl.rcParams['figure.figsize'] = (8,6)
mpl.rcParams['font.size'] = 12

Lund_content = pd.read_csv("Stadsparken-Lund_Skane_County3.csv", header = None)
Lund_content.columns = list('abcdefghi')
#print(Lund_content.head())
translator = Translator()
orginal = "vad heter du"
output = translator.translate(orginal, src = 'sv', dest ='en' )
print(output)
'''
Lund_content['eng'] = Lund_content['i'].apply(translator.translate, dest='en')
Lund_content['words'] = Lund_content['eng'].str.replace('[\W_]+',' ')
Lund_content['words'] = Lund_content['words'].str.split()
#Lund_content['words'] = Lund_content['words'].str.split('[\W_]+')



print(Lund_content.head)
rows = list()
for row in Lund_content[['a','words']].iterrows():
    r = row[1]
    #print(r.words)
    #print(pos_tag(r.words))
    
    for word, pos in pos_tag(r.words):
        #pos = pos_tag(word)
        if pos == 'NN':
            rows.append((r.a, word))

words = pd.DataFrame(rows, columns=['a','word'])
words = words[words.word.str.len() > 0]
words['word'] = words.word.str.lower()

counts = words.groupby('a').word.value_counts().to_frame()\
         .rename(columns = {'word': 'n_w'})

print(counts.head)

counts.to_csv("word_counting/Lund_content_word_counting_NN_trans.csv")
'''
