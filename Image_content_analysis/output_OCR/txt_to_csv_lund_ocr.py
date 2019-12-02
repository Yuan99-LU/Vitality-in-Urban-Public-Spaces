import os
import csv
import pandas as pd

def write_to_csv(DF):
    DF = DF[['index_ID',"place","author", "date"]]
    DF.to_csv("Lund_OCR_output_shorter.csv",
                sep=',', encoding="utf-8", index = False,
                header = False, mode = "w")
    return DF

D_index = pd.read_csv("../images/author_date_png.txt", header = None)
index_ID = D_index[0].apply(lambda x: x[-14:-4]).tolist()
print(index_ID[0:5])


content = []
index_pic = []
f = open('Lund_image_OCR_shorter.txt', 'r', encoding='utf-8')
text1 = f.read()
#print(text1)

#print(text1[0:10])
#text2 = csv.reader(f)
index_pic2 = text1.split('\x0c')
print(index_pic2[0:10])

print(len(index_pic2))
N = 0

places = []
authors = []
dates = []
for OCR_for_each_pic in index_pic2[0: -1]:
    lines = OCR_for_each_pic.split('\n')
    place = ''
    author = ''
    date = ''
    content = []
    for line in lines:
        if(line.find('Photo') != -1):
            date = line.split('-')[-1]
        elif(line.find('Street View') != -1):
            date = 's_' + line.split('-')[-1]
        elif(line != [] and line != [' '] and len(line)>3):
            content.append(line)
            if(len(content)>=2):
                place = content[0]
                author = content[1]
            elif(len(content)==1):
                place = content[0]
                author = content[0]
    places.append(place)
    authors.append(author)
    dates.append(date)
           

DF_out = pd.DataFrame({'index_ID':index_ID, 'place': places,'author': authors, 'date': dates})
write_to_csv(DF_out)
#content_split = content.split('\x0c')
#print(content_split[0:10])

