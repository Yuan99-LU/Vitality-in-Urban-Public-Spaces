import pandas as pd
import timeit
import re

data = pd.read_csv('Lund_OCR_and_content_analysis.csv')

print(data.head(2))

data['year']= data['date'].apply(lambda x: str(x).strip('_s').split()[1]
                                 if str(x)!='' and str(x) not in ['Photo', 's_Street View'] else None)
data['month']= data['date'].apply(lambda x: str(x).strip('_s').split()[0]
                                  if str(x)!='' and str(x) not in ['Photo', 's_Street View'] else None)
print(data['year'].head(100))

data.to_csv('Lund_OCR_and_content_analysis_split_year_month.csv')
