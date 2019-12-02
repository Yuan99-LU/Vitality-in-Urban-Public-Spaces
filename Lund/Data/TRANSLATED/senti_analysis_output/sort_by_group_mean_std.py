import pandas as pd

data1 = pd.read_csv('all_184_rebasic_senti_analysis.csv')

#data = data.sort_values(by = ['a', 'n_w'], ascending=[0,0])
data = data1[['review language','rating score', 'basic_sentiment_text', 'basic_sentiment_title', 'author contributions', 'author_votes']]
data_mean = data.groupby('review language').mean()
data_mean.columns = [['rating_csore_mean', 'basic_sentiment_text_mean', 'basic_sentiment_title_mean', 'author_contributions_mean', 'author_votes_mean']]
#print(data_mean)
#data = data.sort_values(by = ['e'], ascending=[1])
#data = data.sort_values(by = ['a'], ascending=[0])
#print(data_mean)
#data_std = data.groupby('').std()
#data_std.columns = [['e_std', 'c_std', 'd_std', 'basic_sentiment_std']]
#print(data_std)

#data_new = pd.concat([data_mean, data_std], axis = 1)
print(data_mean)

data_mean.to_csv('output/sort_by_group_mean_restaurants.csv')
