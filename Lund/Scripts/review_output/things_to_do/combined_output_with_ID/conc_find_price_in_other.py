import pandas as pd
import os
import numpy as np


data1 = pd.read_csv('Lund_to_do_things_overview.csv')

data2= pd.read_csv('_to_do_things_list_with_ID_name.csv',
                   names = ['poi_name', 'poi_id','review language', 'review count by language',
                            'author contributions', 'author_votes','rating score', 'rating date',
                            'rating title', 'rating place', 'text'])

print(data2.head(1))

data3 = data2.groupby('poi_id')
#print(data3.describe())
#print(data3.count())
#for key, item in data3:
#    print(data3.get_group(key), '\n\n')
#print(data3.head(3))

data2['total review count'] = data2['poi_id']
data2['average rating score'] = data2['poi_id']
data2['price'] = data2['poi_id']
data2['address'] = data2['poi_id']
data2['postcode'] = data2['poi_id']
data2['category'] = data2['poi_id']
for url in data1['url']:
    #print(url)
    total_review_count = data1[data1['url']== url]['review count'].values[0]
    average_score = data1[data1['url']== url]['aggregating rating value'].values[0]
    price_range = data1[data1['url']== url]['price range'].values[0]
    address = data1[data1['url']== url]['address'].values[0]
    postcode = data1[data1['url']== url]['postcode'].values[0]
    category = data1[data1['url']== url]['category'].values[0]
    
    data2['total review count'] = data2['total review count'].apply(lambda x: total_review_count if (str(x) in url) else x)
    data2['average rating score'] = data2['average rating score'].apply(lambda x: average_score if (str(x) in url) else x)
    data2['price'] = data2['price'].apply(lambda x: price_range if (str(x) in url) else x)
    data2['address'] = data2['address'].apply(lambda x: address if (str(x) in url) else x)
    data2['postcode'] = data2['postcode'].apply(lambda x: postcode if (str(x) in url) else x)
    data2['category'] = data2['category'].apply(lambda x: category if (str(x) in url) else x)
    
print(data2['price'])


data2 = data2[['poi_name', 'poi_id', 'total review count', 'average rating score', 'price',
               'address', 'postcode', 'category', 'review language', 'review count by language',
                            'author contributions', 'author_votes','rating score', 'rating date',
                            'rating title', 'rating place', 'text']]
print(data2.head(1))

data2.to_csv('./' + 'things_to_do_in_Lund_add_price_address_etc' +'.csv', mode = 'w', index= False)
