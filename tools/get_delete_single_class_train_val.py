'''
Author: Jian Du
Date: 2019_8_8
Tel：15088315628

This File use to creat train.txt and val.txt for one class.
INFO:1.file "data/all_label" suoulde have "Annotations.txt"
     2.data of picture is in many Files,not in oen file
     3.Always,this file can delete one class,if you need.
'''

import os
need_class=9 # begin with 0
path='./'


#dir
dir_file_annotaioon = './7.txt'
dir_file_val=path+str(need_class)+'.txt'


File = open(dir_file_annotaioon,'r',encoding='utf-8')
File2 =  open(dir_file_val,'w',encoding='utf-8')

lines = File.readlines()
index=0
for line in lines:
    w=int((len(line.split(' '))-1)/5)
    bool_word = 0
    for i in range(w):
        print(i)
        if line.split(' ')[i*5+1] != str(need_class):
            if bool_word==0:
                if index==0:
                    print(0)
                else:
                    File2.write('\n')
                File2.write(line.split(' ')[0].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 1].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 2].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 3].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 4].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 5].strip('\n'))
                bool_word=1
            else:
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 1].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 2].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 3].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 4].strip('\n'))
                File2.write(' ')
                File2.write(line.split(' ')[i * 5 + 5].strip('\n'))
    index=index+1


