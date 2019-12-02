from PIL import Image
from io import BytesIO

img = Image.open("Lund_00001.png")
xmin = 920
ymin = 20
xmax = 1300
ymax = 190
img_crop = img.crop((int(xmin), int(ymin), int(xmax), int(ymax)))
img_crop.save("crop.png")
