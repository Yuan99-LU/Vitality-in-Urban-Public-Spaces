import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as mpl
#import matplotlib.use

mpl.style.use('ggplot')
mpl.rcParams['figure.figsize'] = (8,6)
mpl.rcParams['font.size'] = 12

Lund_content = pd.read_csv("Stadsparken-Lund_Skane_County3.csv", header = None)
Lund_content.columns = list('abcdefghi')
print(Lund_content.head())
#Lund_content = Lund_content.drop('a', axis = 1)
#count = pd.Series(Lund_content.squeeze().values.ravel()).value_counts()
#print(Lund_content['i'])
Lund_content['words'] = Lund_content['i'].str.split('[\W_]+')
#print(Lund_content)
#count = pd.Series(Lund_content['i'].squeeze().values.ravel()).value_counts()
#count = Lund_content['i'].value_counts()
#output = pd.DataFrame({'Measure': count.index, 'Count':count.values, 'Percentage':(count/count.sum()).values})
#print(Lund_content[1].value_counts())
#print(output.head())
#output.to_csv("word_counting/Lund_content_word_counting.csv")

rows = list()
for row in Lund_content[['a','words']].iterrows():
    r = row[1]
    for word in r.words:
        rows.append((r.a, word))

words = pd.DataFrame(rows, columns=['a','word'])
#print(words.head())

words = words[words.word.str.len() > 0]
#print(words.head())

words['word'] = words.word.str.lower()
print(words.head())

counts = words.groupby('a').word.value_counts().to_frame()\
         .rename(columns = {'word': 'n_w'})

print(counts.head)

counts.to_csv("word_counting/Lund_content_word_counting.csv")
