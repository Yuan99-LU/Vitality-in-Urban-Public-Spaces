import pandas as pd

data = pd.read_csv('intersection lookpoint.csv')

#print(data.head(5))

data_b= data['b']
data_c= data['c']
names = ['b','c', 'd', 'e','f','g','h','i','j','k']
data_group= []
for name in names:
    data_new = data[name]
    data_group.append(data_new)
data_new_all = pd.concat(data_group)

data_count = data_new_all.value_counts()

data_count.to_csv('intersection lookpoint_counting.csv')

