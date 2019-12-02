import pandas as pd

data1 =  pd.read_csv('intersection lookpoint.csv')
data2 = pd.read_csv('Lund_OCR_and_PhotoInfo_no_ref_code.csv')

print(data1.shape)
print(data2.shape)

data3 = pd.merge(data1, data2, left_on='ID',right_on ='index_ID', how='left')

print(data3.shape)

data3.to_csv('Lund_OCR_and_content_analysis.csv')
