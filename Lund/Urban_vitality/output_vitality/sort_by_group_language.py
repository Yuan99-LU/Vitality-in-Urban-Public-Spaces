import pandas as pd

data = pd.read_csv('"urban vitality".csv', names = 'abcdef')

print(data.head(5))
data = data[['a','b']]
mean = data.groupby('a').max()

print(mean)
#print(mean['a'])
#count = data_orig.groupby('language').language.value_counts().rename(columns = {'language','language_o','count'})
#print(count)
#print(count)
#data = data.sort_values(by = ['e'], ascending=[1])
#data = data.sort_values(by = ['a'], ascending=[0])

mean.to_csv('sort_output/"urban_vitality"_numbers.csv')
