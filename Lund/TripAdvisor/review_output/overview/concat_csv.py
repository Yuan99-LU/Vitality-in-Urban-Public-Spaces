import pandas as pd
import os

file_names = [x for x in os.listdir('.') if (x.endswith('.csv'))]

print(file_names)
print(len(file_names))
data_with_header = pd.read_csv(file_names[2])
header = data_with_header.columns.values
print(header)
data=[]

for file_name in file_names:
    N = file_names.index(file_name)
    if(N ==2):
        data_t = pd.read_csv(file_name)
        data.append(data_t)
    else:
        data_t = pd.read_csv(file_name, names= header)
        data.append(data_t)
    print(data_t.head(1))
    


data_new = pd.concat(data)
#print(data_new.head(1))
data_new.to_csv('combined_output/restaurant_overview_Lund.csv', mode = 'w', header = True, index= False)

#print(data1.head())

