import pandas as pd

data1 = pd.read_csv('sort_by_group_mean_restaurants.csv')
data2 = pd.read_csv('sort_by_group_counts_restaurants.csv', names = ['language1', 'language', 'count'])
data2 = data2[['language1', 'count']]

data_new = pd.concat([data1, data2], axis =1)

data_new.to_csv('sort_by_group_mean_count_restaurants.csv', index = False)
