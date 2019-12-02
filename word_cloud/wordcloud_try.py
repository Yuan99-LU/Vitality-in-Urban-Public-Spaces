from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

from PIL import Image
import os
import pandas as pd

file_names = [x for x in os.listdir('concat_out') if x.endswith('.csv')]

for file_name in file_names:
    data = pd.read_csv('concat_out/'+file_name,
                       names = ['index', 'features'])

    data = data.fillna(0)

    print(data.head())
    text_list = data['features'].tolist()
    text = ' '.join(str(e) for e in text_list if e!=0)
    #print((text))
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.show()
    plt.savefig('wordcloud_out/' +file_name[0:-4] +'.png')

