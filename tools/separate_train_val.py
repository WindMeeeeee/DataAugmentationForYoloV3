'''
Author: Jian Du
Date: 2019_7_22
Tel：15088315628
introduction：Use this script ,please satisfy the conditions:   1.have annotation.txt   2.data of picture is in many Files,not in oen file
'''

import os
path='./'
list=[]
list_data=[]
list_data_index=-1
Scale=15               #train/val

create_list=[]
write_list=[]
data_write_list=[]
write_list_index=0

#dir
dir_file_annotaioon = '../data/all_label/1_airSwitch___0_WP/Annotations.txt'
dir_file_train = '../data/all_label/1_airSwitch___0_WP/train.txt'
dir_file_val='../data/all_label/1_airSwitch___0_WP/val.txt'



if os.path.exists(dir_file_train) or os.path.exists(dir_file_val):
    print('train.txt or val.txt is exist!!!Please delete')
else:
    train=open(dir_file_train,'w',encoding='utf-8')
    val=open(dir_file_val,'w',encoding='utf-8')
    File=open(dir_file_annotaioon,'r',encoding='utf-8')
    lines=File.readlines()
    for line in lines:
        write_list.append(line)
        name_file=[]
        for name in line.split("\\"):
            name_file.append(name)
        #print(name_file[2])
        if name_file[2] not in list:
            list_data_index=list_data_index+1
            list_data.append(1)
            list.append(name_file[2])
        else:
            list_data[list_data_index]=list_data[list_data_index]+1
    print('*'*20)
    print("From Annotations.txt ,There ara %d Files:"%(len(list)))
    for class_name in list:
        print(class_name+':'+str(list_data[list.index(class_name)]))
    bool_train=0
    bool_val=0
    for i in range(len(list)):
        val_index=0
        data_write_list.append(i)
        for x in range(0,list_data[i]):
            if x%Scale==0:
                if bool_val==0:
                    val.write(write_list[write_list_index].strip('\n'))
                else:
                    val.write('\n')
                    val.write(write_list[write_list_index].strip('\n'))       #val
                write_list_index=write_list_index+1
                val_index=val_index+1
                data_write_list[i]=val_index
                bool_val=1
            else:
                if bool_train ==0:
                    train.write(write_list[write_list_index].strip('\n'))
                else:
                    train.write('\n')
                    train.write(write_list[write_list_index].strip('\n'))     #train
                write_list_index=write_list_index+1
                bool_train=1
    val.close()
    train.close()
    print('*'*20)
    print('Scale is %d'%(Scale))
    print('*'*20)
    for i in range(len(list)):
        print(list[i]+':'+str(data_write_list[i])+'(val)'+','+str(list_data[i]-data_write_list[i])+'(train)')