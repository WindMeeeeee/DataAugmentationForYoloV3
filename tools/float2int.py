import os 
import shutil
#float 2 int

file=open('train_NEW.txt','r',encoding='utf-8')
w= open('123.txt','w',encoding='utf-8')
index=0
for line in file.readlines():
    w.write(line.split(' ')[0])

    for i in range(1,len(line.split(' '))):
        for x in line.split(' ')[i].split(','):
            if index==0:
                w.write(' ')
                index=1
            else:
                w.write(',')
            aaa=str(int(float(x)))
            w.write(aaa)
        index=0
    w.write('\n')

#one by one 
#according AAU.txt to get picture
'''
file= open('AAU.txt','r',encoding='utf-8')
path = './AAU/'
for line in file.readlines():
    file_path=line.split(' ')[0]
    for i in file_path.split(' '):
        #print(i)
        name=i.split('\\')[6]
        path2=path+name
        print(path2)
        break
    #shutil.move(file_path,dst_path)
    shutil.copy(file_path,path2)
'''
