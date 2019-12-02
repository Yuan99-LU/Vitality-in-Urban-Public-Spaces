import pandas as pd

data  = pd.read_csv('Botanical_Gardens_Botaniska_Tradgarden-complete.csv', header = None)

print(data.index[-17:-5])
data_new = data.drop(data.index[-17:-13])

data_new.to_csv("Botanical_Gardens_Botaniska_Tradgarden2.csv")
