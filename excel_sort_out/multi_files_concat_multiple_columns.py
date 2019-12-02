import pandas as pd
import os

file_names = [x for x in os.listdir('Gmail/') if x.endswith('.csv')]

for file_name in file_names:

    data = pd.read_csv('Gmail/'+file_name)

    #print(data.head(5))

    #data_b= data['b']
    #data_c= data['c']
    names = ['b','c', 'd', 'e','f','g','h','i','j','k']
    data_group= []
    for name in names:
        data_new = data[name]
        data_group.append(data_new)
    data_new_all = pd.concat(data_group)

    #data_count = data_new_all.value_counts()

    data_new_all.to_csv('concat_out/'+file_name[0:-4] +'_concat.csv')

