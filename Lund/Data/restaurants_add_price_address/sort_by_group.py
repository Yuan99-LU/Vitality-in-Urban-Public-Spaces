import pandas as pd

data = pd.read_csv('all_184_restaurants_in_Lund_add_price_address_etc.csv')

#data = data.sort_values(by = ['a', 'f'], ascending=[0,1])
data_low = data[data['price']== '$$$$']

data_low = data_low.groupby('review language').count()

print(data_low)

data_low.to_csv('sort_by_group_high_price.csv')
