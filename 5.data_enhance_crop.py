import os
import random
from PIL import Image 
file = open('./OUT_PUT/Annotations.txt','r',encoding='utf-8')
lines = file.readlines()
out_put = open('./OUT_PUT/data_enhance_crop/data_enhance_crop.txt','w',encoding='utf-8')

rand_index=0
mode=1
for line in lines:   #one line one picture
    scale = random.uniform(0.2,0.8)
    line = line.strip('\n')
    img_path=''

    index=0     #for calculate
    Xmin=0      #picture's rect position
    Ymin=0
    Xmax=0
    Ymax=0
    pic_w=0     #picture size
    pic_h=0
    for i in line.split(' '):
        if len(i.split(','))<2:
            #open picture 
            img_path=i
        else:
            if index ==0:
                Xmin=int(i.split(',')[0])
                Ymin=int(i.split(',')[1])
                Xmax=int(i.split(',')[2])
                Ymax=int(i.split(',')[3])
            else:
                #print(i.split(',')[0])
                if int(i.split(',')[0])<Xmin:
                    Xmin=int(i.split(',')[0])
                if int(i.split(',')[1])<Ymin:
                    Ymin=int(i.split(',')[1])
                if int(i.split(',')[2])>Xmax:
                    Xmax=int(i.split(',')[2])
                if int(i.split(',')[3])>Ymax:
                    Ymax=int(i.split(',')[3])
            index=index+1
    pic = Image.open(img_path)
    pic_w = pic.size[0]
    pic_h = pic.size[1]
    rand_index = rand_index + 1
    #print(Xmin)
    #print(Ymin)
    #print(Xmax)
    #print(Ymax)
    if mode==1:
        crop_x = int(min(Xmax,pic_w))
        crop_y = int(min(Ymax,pic_h))
        pic = pic.crop((0,0,crop_x,crop_y))
        pic.save('./OUT_PUT/data_enhance_crop/data/'+img_path.split('\\')[-1].split('.')[0]+'C.jpg')
        for a in line.split(' '):
            index_2 = 0
            if len(a.split(','))<2:
                out_put.write(a.split('.jpg')[0]+'C.jpg')
            else:
                for xx in range(0,5):
                    if index_2 == 0:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[4])))
                    elif index_2 == 4:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[index_2-1])))
                    else:
                        out_put.write(' ')
                        #print(i.split(',')[index])
                        out_put.write(str(int(a.split(',')[index_2-1])))
                    index_2 = index_2 + 1

    elif mode==2:
        crop_x=int(Xmin)
        crop_y=int(min(Ymax,pic_h))
        pic = pic.crop((crop_x,0,pic_w,crop_y))
        pic.save('./OUT_PUT/data_enhance_crop/data/'+img_path.split('\\')[-1].split('.')[0]+'C.jpg')
        for a in line.split(' '):
            index_2 = 0
            if len(a.split(','))<2:
                out_put.write(a.split('.jpg')[0]+'C.jpg')
            else:
                for xx in range(0,5):
                    if index_2 == 0:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[4])))
                    elif index_2 == 4 or index_2 == 2:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[index_2-1])))
                    else:
                        out_put.write(' ')
                        #print(i.split(',')[index])
                        out_put.write(str(int(a.split(',')[index_2-1])-crop_x))
                    index_2 = index_2 + 1
    
    elif mode==3:
        crop_x=int(min(Xmax,pic_w))
        crop_y=int(max(Ymin,0))
        pic = pic.crop((0,crop_y,crop_x,pic_h))
        pic.save('./OUT_PUT/data_enhance_crop/data/'+img_path.split('\\')[-1].split('.')[0]+'C.jpg')
        for a in line.split(' '):
            index_2 = 0
            if len(a.split(','))<2:
                out_put.write(a.split('.jpg')[0]+'C.jpg')
            else:
                for xx in range(0,5):
                    if index_2 == 0:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[4])))
                    elif index_2 == 2 or index_2 == 4:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[index_2-1])-crop_y))
                    else:
                        out_put.write(' ')
                        #print(i.split(',')[index])
                        out_put.write(str(int(a.split(',')[index_2-1])))
                    index_2 = index_2 + 1
    elif mode==4:
        crop_x=int(Xmin)
        crop_y=int(Ymin)
        pic = pic.crop((crop_x,crop_y,pic_w,pic_h))
        pic.save('./OUT_PUT/data_enhance_crop/data/'+img_path.split('\\')[-1].split('.')[0]+'C.jpg')
        for a in line.split(' '):
            index_2 = 0
            if len(a.split(','))<2:
                out_put.write(a.split('.jpg')[0]+'C.jpg')
            else:
                for xx in range(0,5):
                    if index_2 == 0:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[4])))
                    elif index_2 == 2 or index_2 == 4:
                        out_put.write(' ')
                        out_put.write(str(int(a.split(',')[index_2-1])-crop_y))
                    else:
                        out_put.write(' ')
                        #print(i.split(',')[index])
                        out_put.write(str(int(a.split(',')[index_2-1])-crop_x))
                    index_2 = index_2 + 1
    mode = mode+1
    if mode==5:
        mode=1

    out_put.write('\n')
    print(img_path.split('\\')[-1].split('.')[0])