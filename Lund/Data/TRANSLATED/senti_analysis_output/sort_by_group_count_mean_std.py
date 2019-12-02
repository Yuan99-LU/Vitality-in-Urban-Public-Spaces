import pandas as pd

data1 = pd.read_csv('all_184_rebasic_senti_analysis.csv')

#data = data.sort_values(by = ['a', 'n_w'], ascending=[0,0])
data = data1[['review language','rating score', 'basic_sentiment_text', 'basic_sentiment_title']]
#mean = data.groupby('a').mean()
#print(mean['a'])
data2 = data.groupby('review language')['review language'].value_counts()
#data2.rename(columns= {'a','language','count'})
#print(data2['review language'])
#print(count)
#print(count)
#data = data.sort_values(by = ['e'], ascending=[1])
#data = data.sort_values(by = ['a'], ascending=[0])

data2.to_csv('output/sort_by_group_counts_restaurants.csv')
