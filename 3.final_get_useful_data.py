import os
from shutil import copyfile
try:
    copyfile('./data/data_configs/class.names', './OUT_PUT/names.txt')
    print('class.names  Files  Sucess!!!!!!')
except Exception as e:
    print(e)
    print('class.names  Files  Fail!!!!!!')
try:
    copyfile('./data/data_configs/yolo_anchors.txt', './OUT_PUT/yolo_anchors.txt')
    print('yolo_anchors.txt  Files  Sucess!!!!!!')
except Exception as e:
    print(e)
    print('yolo_anchors.txt  Files  Fail!!!!!!')

file_src=open('./data/data_configs/annotations.txt','r',encoding='utf-8')
file_tar=open('./OUT_PUT/Annotations.txt','w',encoding='utf-8')
lines=file_src.readlines()
try:
    for line in lines:
        index=0
        line=line.strip('\n')
        while index<(len(line.split(' '))):
            list = line.split(' ')
            if index==0:
                file_tar.write(list[0])
            elif index%5==0:
                file_tar.write(list[index-4])
            elif index%5==1:
                file_tar.write(' ')
                file_tar.write(list[index+1])
                file_tar.write(',')
            else :
                file_tar.write(list[index+1])
                file_tar.write(',')
            index=index+1
        file_tar.write('\n')
    print('Annotations.txt  Files  Sucess!!!!!!')
except Exception as e:
    print(e)
    print('Annotations.txt  Files  Fail!!!!!!')