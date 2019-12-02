import pandas as pd
import os

url_list = ['https://www.tripadvisor.com/Attraction_Review-g189838-d319367-Reviews-Lund_Cathedral-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d319374-Reviews-Botanical_Gardens_Botaniska_Tradgarden-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d267409-Reviews-Kulturen_in_Lund_Museum_of_Cultural_History_and_Open_Air_Museum-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10134259-Reviews-Skrylle_Nature_reserve-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d4743755-Reviews-Skissernas_Museum_Museum_of_Artistic_Process_and_Public_Art-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d8126652-Reviews-Stadsparken-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d9750031-Reviews-Lund_University_Main_Building-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d735398-Reviews-All_Saints_Church_Lund-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d1889146-Reviews-Jakriborg-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d9984402-Reviews-The_Museum_of_Life-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10055631-Reviews-Lundagard_Park-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d319381-Reviews-Lund_University_Historical_Museum_Historiska_Museet-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d3561715-Reviews-Vattenhallen_Science_Center-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d319372-Reviews-Medieval_Museum_Drottens_Museet-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d8594321-Reviews-Rinnebacksravinen-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d9725958-Reviews-Klosterkyrkan-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10525977-Reviews-Kungshuset_i_Lundagard-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d11695775-Reviews-Martenstorget-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10485080-Reviews-Krognoshuset-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10464969-Reviews-Hallestads_kyrka-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d12716657-Reviews-Lund_Tourist_Center-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10556972-Reviews-Nasoteket-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d9750075-Reviews-The_Tegner_Museum-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d14161767-Reviews-Stadsparken-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10611465-Reviews-Rabysjon_och_Raby_Sjopark-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10526091-Reviews-Ostra_kyrkogarden-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10446504-Reviews-Klosterangshojden-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10588825-Reviews-Domkyrkoforum-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d10446502-Reviews-Bjeredsparken-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d12642023-Reviews-Billebjer-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d4291638-Reviews-Hogevall-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d13452023-Reviews-Skrylleslingan-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d15606731-Reviews-Clemenstorget-Lund_Skane_County.html',
'https://www.tripadvisor.com/Attraction_Review-g189838-d15273490-Reviews-Sparbanken_Skane_Arena-Lund_Skane_County.html',]

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

data_new.to_csv('../combined_output_with_ID/' + '_to_do_things_list_with_ID_name.csv', mode = 'w', header = None, index= False)
