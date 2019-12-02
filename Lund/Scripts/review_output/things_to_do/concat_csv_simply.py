import pandas as pd
import os



#file_names = [x for x in os.listdir('../') if (x.endswith('.csv'))]


data1 = pd.read_csv('Botanical_Gardens_Botaniska_Tradgarden-Lund_Skane_County.csv', header =None)
data2 = pd.read_csv('Botanical_Gardens_Botaniska_Tradgarden-ID-d319374complete_languages.csv', header =None)



data_new = pd.concat([data1, data2])
#data_new = data_new[['name', 'id', 0, 1, 2, 3, 4, 5, 6,7, 8]]
print(data_new.head(1))

data_new.to_csv('Botanical_Gardens_Botaniska_Tradgarden-complete' +'.csv', mode = 'w', header = None, index= False)
