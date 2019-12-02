import os
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import numpy as np
import re


def clean_data(text):
    #removing links and special characters using regex
    output_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())   
    return output_text

def analyze_basic_sentiment(text):
    analysis = TextBlob(clean_data(text))
    return analysis.sentiment.polarity

def analyze_bayes_sentiment(text):
    analysis = TextBlob(clean_data(text), analyzer = NaiveBayesAnalyzer())
    print("bayes sentiment is in processing")
    return analysis.sentiment.classification, analysis.sentiment.p_pos, analysis.sentiment.p_neg




file_names = [x for x in os.listdir('.') if not (x.startswith('.'))
              and (x.endswith('.csv'))]

for file_name in file_names[0:1]:
    print(file_name)
    data = pd.read_csv(file_name)
    print(data['eng_text'].head())
    data['basic_sentiment'] = np.array([ analyze_basic_sentiment(text) for text in data['eng_text'] ])
    print("basic sentiment analysis is ready")

    data_new = pd.DataFrame(np.array([ analyze_bayes_sentiment(text) for text in data['eng_text'] ]),
                            columns = ['bayes_class', 'bayes_pos', 'bayes_neg'])

    data['bayes_class'], data['bayes_pos'],data['bayes_neg'] = data_new['bayes_class'], data_new['bayes_pos'],data_new['bayes_neg']
    
    print(data.head())
    data.to_csv("senti_analysis_output/" + file_name[0:-4] + "_senti_analysis.csv")
    
