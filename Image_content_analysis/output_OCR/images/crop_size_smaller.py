from PIL import Image
from io import BytesIO
import os

img_names = [x for x in os.listdir('./author_date/') if (x.endswith('.png'))]

sort_names = sorted(img_names)

FOLDER = 'author_date2/'
if not os.path.exists('./'+FOLDER):
    os.makedirs('./'+FOLDER)
    
for img_name in sort_names:
    img = Image.open('author_date/' + img_name)
    xmin = 0
    ymin = 0
    xmax = 240
    ymax = 200
    img_crop = img.crop((int(xmin), int(ymin), int(xmax), int(ymax)))
    img_crop.save(FOLDER + img_name)
