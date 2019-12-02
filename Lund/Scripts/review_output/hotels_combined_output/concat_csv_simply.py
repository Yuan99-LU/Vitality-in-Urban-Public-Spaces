import pandas as pd
import os



file_names = [x for x in os.listdir('../') if (x.endswith('.csv'))]

print(file_names)
print(len(file_names))

data=[]

for file_name in file_names:
    
    data_t = pd.read_csv('../'+file_name, header =None)
    #print(data_t.head(1))
    N = len(data_t)
    print(N)
    
    
    data.append(data_t)



data_new = pd.concat(data)
#data_new = data_new[['name', 'id', 0, 1, 2, 3, 4, 5, 6,7, 8]]
print(data_new.head(1))

data_new.to_csv('../combined_output/' + '25_hotels_in_Lund' +'.csv', mode = 'w', header = None, index= False)
