import pandas as pd

data1 = pd.read_csv('sort_by_group.csv')

#data = data.sort_values(by = ['a', 'n_w'], ascending=[0,0])
data = data1[['a','e']]
mean = data.groupby('a').mean()
#print(mean['a'])
#count = data.groupby('a').a.value_counts()
#.to_frame.rename(columns = {'a','language','count'})
#print(count)
#print(count)
#data = data.sort_values(by = ['e'], ascending=[1])
#data = data.sort_values(by = ['a'], ascending=[0])

mean.to_csv('sort_by_group_mean_no_sort.csv')
