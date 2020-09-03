import os 
import shutil
#float 2 int

file=open('123.txt','r',encoding='utf-8')
list_2=[]
index=0
for line in file.readlines():


    for i in range(1,len(line.split(' '))):
        index_sec=0
        for x in line.split(' ')[i].split(','):
            if index_sec==4:
                xx=x.split('\n')[0]
                if xx not in list_2:
                    list_2.append(xx)
            index_sec=index_sec+1
        
        index_sec=0
print(list_2)
