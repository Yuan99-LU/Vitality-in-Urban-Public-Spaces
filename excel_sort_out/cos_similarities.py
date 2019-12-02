import pandas as pd

data = pd.read_csv('Lund_OCR_and_content_analysis_split_year_month2.csv')

#print(data.head(-150))
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
          'Oct', 'Nov', 'Dec']

#for i in range(2003, 2019):  #by year
for i in months: #by month
    data2 = data[data['month'] == i]  #by month
    #data2 = data[data['year'] == i]   #by year
    print(data2.shape)

    names = ['b','c', 'd', 'e','f','g','h','i','j','k']
    data_group= []
    for name in names:
        data_new = data2[name]
        data_group.append(data_new)
    data_new_all = pd.concat(data_group)

    data_count = data_new_all.value_counts()

    data_count.to_csv('count_by_month/'+ str(i) +'_counting.csv') #by month
    #data_count.to_csv('count_by_year/'+ str(i) +'_counting.csv') #by year
 
