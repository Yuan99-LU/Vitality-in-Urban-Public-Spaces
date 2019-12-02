import os
import csv
import pandas as pd

def write_to_csv(DF):
    DF = DF[["place","author", "date"]]
    DF.to_csv("Lund_OCR_output.csv",
                sep=',', encoding="utf-8", index = False,
                header = False, mode = "w")
    return DF

D_index = pd.read_csv("../images/author_date_png.txt", header = None)
index_ID = D_index[0].apply(lambda x: x[-14:-4]).tolist()
print(index_ID[0:5])


content = []
index_pic = []
f = open('Lund_image_OCR2.txt', 'r', encoding='utf-8')
text1 = f.read()
#print(text1)

#print(text1[0:10])
#text2 = csv.reader(f)
index_pic2 = text1.split('\x0c')
print(index_pic2[0:10])

print(len(index_pic2))
N = 0


for OCR_for_each_pic in index_pic2[0:1]:
    lines = OCR_for_each_pic.split('\n')
    print(lines)
    #if(line != [] and line != [' '] and len(line[0])>1):
    content.append(line)
    
    if(str(line).find(r'\x0c\x0c')!=-1):
            #print('OK')
        index_pic.append(N)
        index_pic.append(N)
    elif(str(line).find(r'\x0c')!=-1):
        index_pic.append(N)


N += 1
            
    
print(index_pic[-1])
if(index_pic[-1]<N):
    index_pic.append(N)
f.close()
print(len(index_pic))

print(content[0:100])
place = ['']*len(index_pic)
date = ['']*len(index_pic)
author = ['']*len(index_pic)

'''
for i in range(0, len(index_pic)):
    N_index = index_pic[i]
    if(i>0):
        pre_N_index = index_pic[i-1]
    if(i==0):
        pre_N_index = 0
    #print(N_index)
    #print(content[N_index-1])
    if(str(content[N_index-1]).find('Photo') != -1):
        date[i] = content[N_index-1][0].split('-')[-1]
    elif(str(content[N_index-1]).find('Street View') != -1):
        date[i] = 's_' + content[N_index-1][0].split('-')[-1]
    else:
        date[i] = ''
    #if(str(content[N_index-2]) !=''):
        #author[i] = content[N_index-2])
    #else:
        #author[i] = ''
    if(N_index - pre_N_index >= 2):
        place[i] = content[pre_N_index][0].replace('\x0c','')
        author[i] = content[pre_N_index+1][0]
    else:
        place[i] = ''
        author[i] = ''


DF_out = pd.DataFrame({'index_ID':index_ID, 'place': place,
                       'author': author, 'date': date})
write_to_csv(DF_out)
#content_split = content.split('\x0c')
#print(content_split[0:10])
'''
