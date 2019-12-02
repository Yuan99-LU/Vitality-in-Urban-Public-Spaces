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
    
    res_name = file_name[0 : file_name.find('-ID-')]
    res_id = file_name[file_name.find('-ID-')+4: file_name.find(".csv")]
    print(res_id)

    data_t['name'] = [res_name]*N
    data_t['id'] = [res_id]*N
    #print(data_t['id'][0:5])
    #print(data_t['name'][0:5])
    
    
    data.append(data_t)



data_new = pd.concat(data)
data_new = data_new[['name', 'id', 0, 1, 2, 3, 4, 5, 6,7, 8]]
print(data_new.head(1))

data_new.to_csv('../combined_output/' + 'restaurants-151-180'+'.csv', mode = 'w', header = None, index= False)
