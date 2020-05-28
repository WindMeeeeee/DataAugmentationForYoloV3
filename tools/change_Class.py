import os
file_in=open('./Annotations.txt','r',encoding='utf-8')
file_output=open('./Annotations_NEW.txt','w',encoding='utf-8')

old_list=[3,1]
new_list=[5,9] #plesas one by one.  et. 1,2,3,4 

lines = file_in.readlines()
for line in lines:
    index = len(line.split())
    first=0
    if index>0:
        for mes in line.split():
            if first==0:
                first=1
                file_output.write(mes)

            else:
                class_old=int(mes.split(',')[4])
                if class_old in old_list:
                    need_index = old_list.index(class_old)
                    new_index=new_list[need_index]
                    file_output.write(' ')
                    file_output.write(mes.split(',')[0])
                    file_output.write(',')
                    file_output.write(mes.split(',')[1])
                    file_output.write(',')
                    file_output.write(mes.split(',')[2])
                    file_output.write(',')
                    file_output.write(mes.split(',')[3])
                    file_output.write(',')
                    file_output.write(str(new_index))
                else:
                    file_output.write(' ')
                    file_output.write(mes)
    file_output.write('\n')

                
        