import os
import random
from PIL import Image 
import random

file = open('./OUT_PUT/Annotations.txt','r',encoding='utf-8')
lines = file.readlines()
out_put = open('./OUT_PUT/data_enhance_mixup/data_enhance_mixup.txt','w',encoding='utf-8')
#other data pic
path_other='./OUT_PUT/data_enhance_mixup/other_data'

list_other=[]
for i in os.listdir(path_other):
    list_other.append(i)
len_other=len(list_other)

if len_other==0:
    print('you should put some unuseful picthre in "./OUT_PUT/data_enhance_mixup/other_data" file')
else:
    for line in lines:
        out_put.write(line)
        path='./data/imgs/'+line.split()[0].split('\\')[-1]
        img1 = Image.open(path)
        img1 = img1.convert('RGBA')

        len_other_index = random.randint(0,len_other-1)
        path_other_dir='./OUT_PUT/data_enhance_mixup/other_data/'+list_other[len_other_index]
        img2 = Image.open(path_other_dir)
        img2 = img2.convert('RGBA')
        #resize to size of img1
        img2 = img2.resize(img1.size)
                
        img = Image.blend(img1, img2, 0.1)
        img = img.convert('RGB')
        output_dir='./OUT_PUT/data_enhance_mixup/data/'+line.split()[0].split('\\')[-1].split('.jpg')[0]+"M.jpg"
        img.save(output_dir)
        print(line.split()[0].split('\\')[-1].split('.jpg')[0]+"M.jpg"+"OK!!!")
        img1.close()
        img2.close()
