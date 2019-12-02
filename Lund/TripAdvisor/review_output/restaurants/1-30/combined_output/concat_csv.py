import pandas as pd
import os

url_list = ['https://www.tripadvisor.com/Restaurant_Review-g189838-d740115-Reviews-Govindas_Vegetariska-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d10195575-Reviews-Restaurang_La_Cucina-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d3139458-Reviews-Mat_Destillat-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d7384359-Reviews-Ihsiri-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d6981566-Reviews-Creperiet_i_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d941772-Reviews-Gattostretto-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d3942974-Reviews-Matrummet-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d780405-Reviews-Klostergatans_vin_och_delikatess-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d7195560-Reviews-Matsalen_Grand_Hotel_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d1023140-Reviews-Mediterranean-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d2388076-Reviews-Ra_Epok-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d12097252-Reviews-Restaurant_Pa_Skissernas-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d3194502-Reviews-M_E_A_T-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d11875773-Reviews-Aiko_Sushi-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d7339811-Reviews-Rosegarden_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d2695650-Reviews-Malmstens_fisk-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d10325722-Reviews-Gambrinus-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d8844771-Reviews-Hjulet_Mat_Vin-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d6938337-Reviews-Restaurang_VED-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d2306597-Reviews-Buljong-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d807919-Reviews-Restaurang_Staket-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d796874-Reviews-V_E_S_P_A_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d1043211-Reviews-Restaurang_Sandra-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d8581453-Reviews-Fengsson_Dumplings-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d811774-Reviews-Wasabi-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d10770543-Reviews-Dos_Hermanos-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d12430704-Reviews-Restaurang_Thuy-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d3483544-Reviews-Harrys_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d5936436-Reviews-Ha_Long_Viet_Thai_Restaurang-Lund_Skane_County.html',
'https://www.tripadvisor.com/Restaurant_Review-g189838-d12811361-Reviews-Gamla_Franska-Lund_Skane_County.html']

file_names = [x for x in os.listdir('../') if (x.endswith('.csv'))]

print(file_names)
print(len(file_names))

data=[]

for file_name in file_names:
    
    data_t = pd.read_csv('../'+file_name, header =None)
    #print(data_t.head(1))
    N = len(data_t)
    
    for url in url_list:
        if file_name[0:-5] in url:
            res_name = file_name[0 : file_name.find('-Lund_Skane_County')]
            res_id = url[url.find('_Review-g189838-')+16 : url.find("-Reviews-")]
            print(res_id)

    data_t['name'] = [res_name]*N
    data_t['id'] = [res_id]*N
    #print(data_t['id'][0:5])
    #print(data_t['name'][0:5])
    
    
    data.append(data_t)



data_new = pd.concat(data)
data_new = data_new[['name', 'id', 0, 1, 2, 3, 4, 5, 6,7, 8]]
print(data_new.head(1))

data_new.to_csv('../combined_output/' + res_name + '-ID-' + res_id +'.csv', mode = 'w', header = None, index= False)
