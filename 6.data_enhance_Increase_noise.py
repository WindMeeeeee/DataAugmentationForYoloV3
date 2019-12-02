#Attention:This method will take a lot of time.larger picture take more time
import os
import random
from PIL import Image 
import numpy as np
from skimage import util
import matplotlib

import cv2
file = open('./OUT_PUT/Annotations.txt','r',encoding='utf-8')
lines = file.readlines()
out_put = open('./OUT_PUT/data_enhance_Increase_noise/data_enhance_Increase_noise.txt','w',encoding='utf-8')


for line in lines:
    line = line.strip('\n')
    img_path=''
    for i in line.split(' '):
        if len(i.split(','))==1:
            out_put.write(i.split('.jpg')[0]+'N'+'.jpg')
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
    img = Image.open(img_path,'r')
    
    peppers = cv2.imread(img_path, 0)
    
    
    img = np.array(img)

    #diffrernce method
    noise_img = util.random_noise(img,mode='gaussian')
    #noise_img = util.random_noise(img,mode='salt')
    #noise_img = util.random_noise(img,mode='pepper')
    #noise_img = util.random_noise(img,mode='s&p')
    #noise_img = util.random_noise(img,mode='speckle')

    
    matplotlib.image.imsave('./OUT_PUT/data_enhance_Increase_noise/data/'+img_path.split('\\')[-1].split('.')[0]+'N.jpg', noise_img)
    print(img_path.split('\\')[-1].split('.')[0])
