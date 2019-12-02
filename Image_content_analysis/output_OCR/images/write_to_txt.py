import os

txt_names = [x for x in os.listdir('./author_date/') if (x.endswith('.png'))]

sort_names = sorted(txt_names)

f = open('author_date_png.txt', 'w')
for name in sort_names:
    f.write('images/author_date/' + name + '\n')
f.close()
    

