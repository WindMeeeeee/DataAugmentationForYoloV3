import os 
import shutil
#float 2 int

file=open('predict.txt','r',encoding='utf-8')
w= open('123.txt','w',encoding='utf-8')

for line in file.readlines():
    w.write(line.split(' ')[0])
    w.write(' ')
    for i in range(1,len(line.split(' '))):
        a=float(line.split(' ')[i])
        b=str(int(a))
        w.write(b)
        w.write(' ')
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
