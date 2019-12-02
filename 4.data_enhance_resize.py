import os
import random
from PIL import Image 
file = open('./OUT_PUT/Annotations.txt','r',encoding='utf-8')
lines = file.readlines()
out_put = open('./OUT_PUT/data_enhance_resize/data_enhance_resize.txt','w',encoding='utf-8')

#img = img.resize((width, height))

for line in lines:
    scale = random.uniform(0.2,0.8)
    line = line.strip('\n')
    img_path=''
    for i in line.split(' '):
        if len(i.split(','))==1:
            out_put.write(i.split('.jpg')[0]+'R'+'.jpg')
            img_path=i
        else:
            index = 0
            for x in range(0,5):
                if index == 0:
                    out_put.write(' ')
                    out_put.write(str(int(i.split(',')[4])))
                elif index == 4:
                    out_put.write(' ')
                    out_put.write(str(int(float(i.split(',')[index-1])*scale)))
                else:
                    out_put.write(' ')
                    #print(i.split(',')[index])
                    out_put.write(str(int(float(i.split(',')[index-1])*scale)))
                index = index + 1
    out_put.write('\n')
    img = Image.open(img_path,'r')
    img = img.resize((int(img.size[0]*scale), int(scale*img.size[1])))
    img.save('./OUT_PUT/data_enhance_resize/data/'+img_path.split('\\')[-1].split('.')[0]+'R.jpg')
    print(img_path.split('\\')[-1].split('.')[0])

    