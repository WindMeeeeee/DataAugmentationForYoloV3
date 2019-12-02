import os
import random
from PIL import Image 
import numpy as np
from skimage import util
import matplotlib
import cv2

file = open('./OUT_PUT/Annotations.txt','r',encoding='utf-8')
lines = file.readlines()
out_put = open('./OUT_PUT/data_enhance_Change_Bright/data_enhance_Change_Bright.txt','w',encoding='utf-8')
item=['0.3','0.5','0.7']
for line in lines:
    line = line.strip('\n')
    img_path=''
    for i in line.split(' '):
        if len(i.split(','))==1:
            out_put.write(i.split('.jpg')[0]+'B'+'.jpg')
            img_path=i
        else:
            index = 0
            for x in range(0,5):
                if index == 0:
                    out_put.write(' ')
                    out_put.write(str(int(float(i.split(',')[4]))))
                elif index == 4:
                    out_put.write(' ')
                    out_put.write(str(int(float(i.split(',')[index-1]))))
                else:
                    out_put.write(' ')
                    #print(i.split(',')[index])
                    out_put.write(str(int(float(i.split(',')[index-1]))))
                index = index + 1
    out_put.write('\n')
    im1 = Image.open(img_path)

    
    x_index=float(random.choice(item))
    im2 = im1.point(lambda p: p * x_index)
    im2.save("./OUT_PUT/data_enhance_Change_Bright/data/'+img_path.split('\\')[-1].split('.')[0]+'B.jpg")
'''
im1 = Image.open("1.jpg")
im2 = im1.point(lambda p: p * 0.2)
im2.show()
#im2.save("angelababy2.jpg")
'''