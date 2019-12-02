import pandas as pd

data = pd.read_csv('Botanical_Gardens_Botaniska_Tradgarden2.csv')

data = data.drop(['Unnamed: 0'], axis =1)

print(data.columns)

print(data.head(1))

data.to_csv('Botanical_Gardens_Botaniska_Tradgarden22.csv', header = None, index = False)
