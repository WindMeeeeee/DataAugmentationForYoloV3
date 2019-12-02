# encoding: utf-8

import json
import os
import shutil
from utils.plot_utils import save_labeled_img, get_color_table
import logging
import random

from utils.data_generate import dataGenerater

class dataProcess:
    """
    --data_dir
        --annotations(JSON_FILE)
            --1.json
            --2.json
            ...
        --imgs
            --1.jpg
            --2.jpg
            ...
        --data_configs
            --data_process.log
            --annotation.txt
            --class.names
            --train.txt
            --val.txt
    """
    data_dir, json_dir, img_dir = '', 'annotations', 'imgs'
    data_config_dir = 'data_configs'

    log_path = 'data_process.log'
    annotation_txt_path = 'annotations.txt'
    class_name_path = 'class.names'
    train_txt = ''
    val_txt = ''

    def __init__(self, idata_dir, idata_config_dir=None):
        self.data_dir = idata_dir
        self.json_dir = os.path.join(idata_dir, self.json_dir)
        self.img_dir = os.path.join(idata_dir, self.img_dir)

        if idata_config_dir is None:
            self.data_config_dir = os.path.join(data_dir, self.data_config_dir)
        else:
            self.data_config_dir = idata_config_dir
        self.annotation_txt_path = os.path.join(self.data_config_dir, self.annotation_txt_path)
        self.class_name_path = os.path.join(self.data_config_dir, self.class_name_path)
        if not os.path.isdir(self.data_config_dir):
            os.mkdir(self.data_config_dir)

        self.log_path = os.path.join(self.data_config_dir, self.log_path)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S', filename=self.log_path, filemode='a')
        self.logger = logging.getLogger(__name__)

    def run(self, do_chinese2english=False, do_json2txt=False, do_seperate_trainval=False, do_draw_labeledimgs=False,
            do_data_generate=False,do_send_class_dirs=False):
        if do_chinese2english:
            self.json_img_rename(self.json_dir, self.img_dir, prefix='', startnum=1)
            self.logger.info('do_chinese2english is finished.')
        if do_json2txt:
            #self.json2txt(noannodst_savedir=os.path.join(self.data_config_dir, 'nolabelimgs'),labeled_img_savedir=os.path.join(self.data_config_dir,'labeledimgs'))
            self.json2txt(noannodst_savedir=os.path.join(self.data_config_dir, '../nolabelimgs'),labeled_img_savedir=os.path.join(self.data_config_dir,'../labeledimgs'))
            self.logger.info('do_json2txt is finished.')
        if do_seperate_trainval:
            self.train_txt = os.path.join(self.data_config_dir, 'train.txt')
            self.val_txt = os.path.join(self.data_config_dir, 'val.txt')
            self.separate_train_val(self.annotation_txt_path, self.train_txt, self.val_txt, train_rate=0.9)
            self.logger.info('do_seperate_trainval is finished.')
        if do_draw_labeledimgs:
            save_dir = os.path.join(self.data_config_dir, 'labeled_imgs')
            if not os.path.isdir(save_dir):
                os.mkdir(save_dir)
            self.data_draw_annotxt(self.annotation_txt_path, self.class_name_path, save_dir)
            self.logger.info('do_draw_labeledimgs is finished.')

        if do_data_generate:
            self.train_txt = os.path.join(self.data_config_dir, 'train.txt')
            self.data_generate(self.train_txt, do_flip1=True, do_rot90=False,do_crop=True)
            self.logger.info('do_data_generate is finished.')

    def do_relabel(self, eclassindexes, classnames):
        ori_anno = os.path.join(self.data_config_dir, 'all_annotations.txt')
        # out_classnames_file = os.path.join(self.data_config_dir, 'relabeled_class.names')
        # out_anno_path = os.path.join(self.data_config_dir, 'relabeled_annotation.names')
        shutil.move(self.class_name_path, os.path.join(self.data_config_dir, 'all_class.names'))
        shutil.move(self.annotation_txt_path, os.path.join(self.data_config_dir, 'all_annotations.txt'))
        self.relabel_(ori_anno, self.class_name_path, self.annotation_txt_path, eclassindexes=eclassindexes,
                      classnames=classnames)
        print('do_relabel is finished.')

    def do_send_class_dirs(self, choose_idx=[]):
        dst_dir = os.path.join(self.data_config_dir, 'class_dirs')
        if not os.path.isdir(dst_dir):
            os.mkdir(dst_dir)
        self.send_class_dirs(self.annotation_txt_path, self.class_name_path, dst_dir, choose_idx=choose_idx)

    def json_img_rename(self, json_dir, img_dir, prefix='', startnum=1):
        """文件重命名，去除中文影响"""
        logger = self.logger
        json_names = os.listdir(json_dir)
        c = startnum
        for json_name in json_names:
            pre = prefix + str(c)
            jpath = os.path.join(json_dir, json_name)
            djpath = os.path.join(json_dir, pre + ".json")

            ipath = os.path.join(img_dir, json_name[:-5] + ".jpg")
            dipath = os.path.join(img_dir, pre + ".jpg")
            try:
                os.rename(jpath, djpath)
                os.rename(ipath, dipath)
                c = c + 1
            except:
                info = 'os.rename error:json:{}->{},img:{}->{}'.format(jpath, djpath, ipath, dipath)
                logger.error(info)
                continue
        info = '{} pairs of json and img are renamed.'.format(c)
        logger.info(info)

    def json2txt(self, noannodst_savedir=None, labeled_img_savedir=None):
        # setting loggers
        logger = self.logger
        json_dir = self.json_dir
        annotation_txt = self.annotation_txt_path
        class_name_path = self.class_name_path
        json_names = os.listdir(json_dir)
        annotations = []
        classnames = []
        f_anno = open(annotation_txt, 'w')
        wcount = 0
        for json_name in json_names:
            imgname = json_name[:-5] + ".jpg"
            imgpath = os.path.join(self.img_dir, imgname)
            line = imgpath
            jpath = os.path.join(json_dir, json_name)
            f = open(jpath, encoding='utf-8')
            j = json.load(f)
            box_names = []
            if j['labeled'] is False:
                if noannodst_savedir is not None:
                    dst_file = os.path.join(noannodst_savedir, imgname)
                    shutil.copyfile(imgpath, dst_file)
                info = imgname + ' is not labeled.'
                logger.warning(info)
                wcount += 1
                continue
            else:
                w, h = j['size']['width'], j['size']['height']
                ls = j['outputs']['object']
                for obj in ls:
                    name, box = '', {}
                    for objk in obj:
                        if objk == 'name':
                            name = obj[objk]
                        else:
                            box = obj[objk]

                    if name not in classnames:
                        classnames.append(name)
                        # if name=='power':
                        #     print('power:',imgname)
                    if 'xmin' in box:
                        xmin, ymin, xmax, ymax = max(box['xmin'], 0), max(box['ymin'], 0), min(box['xmax'], w - 1), min(
                            box['ymax'], h - 1)
                    else:
                        xmin, ymin, xmax, ymax = 10000, 10000, 0, 0
                        for key in box:
                            if key[0] == 'x':
                                if box[key] < xmin:
                                    xmin = box[key]
                                if box[key] > xmax:
                                    xmax = box[key]
                            elif key[0] == 'y':
                                if box[key] < ymin:
                                    ymin = box[key]
                                if box[key] > ymax:
                                    ymax = box[key]
                            else:
                                info = json_name + ' has wrong box key(not x or y).'
                                logger.error(info)
                            xmin, ymin, xmax, ymax = max(xmin, 0), max(ymin, 0), min(xmax, w - 1), min(
                                ymax, h - 1)
                    if xmin >= xmax or ymin >= ymax:
                        info = json_name + ' has wrong annotation.'
                        logger.error(info)
                        continue
                    box_names.append([xmin, ymin, xmax, ymax, name])
                    line = line + ' ' + str(classnames.index(name)) + ' ' + str(xmin) + ' ' + str(
                        ymin) + ' ' + str(xmax) + ' ' + str(ymax)

                if len(box_names) == 0:
                    continue
                annotations.append(line)
                f_anno.write(line)
                # logger.info(line)
                f_anno.write('\n')
                print(line)
                if labeled_img_savedir is not None:
                    dst_file = os.path.join(labeled_img_savedir, imgname)
                    color_table = get_color_table(len(classnames))
                    # shutil.copyfile(imgpath, dst_file)
                    save_labeled_img(imgpath, box_names, dst_file, classnames, color_table=color_table)

        f_anno.close()
        info = 'wrong pics:{}'.format(wcount)
        logger.info(info)
        print(info)
        f_class = open(class_name_path, 'w')
        for cla in classnames:
            f_class.write(cla)
            f_class.write('\n')
        f_class.close()
        logger.info('class.names has been saved.')

    @staticmethod
    def separate_train_val(file_name, out_train, out_val, train_rate=0.8):
        content = open(file_name, 'r').readlines()
        random.shuffle(content)
        size = len(content)
        train_size = round(size * train_rate)
        print('size:{},train:{},val:{}'.format(size, train_size, size - train_size))
        with open(out_train, 'w') as f:
            for line in content[:train_size]:
                f.write(line)
        with open(out_val, 'w') as f:
            for line in content[train_size:]:
                f.write(line)

    # @staticmethod
    # def separate_train_val_byclass(file_name,classname_txt, out_train, out_val, train_rate=0.8):
    #     contentc = open(classname_txt, 'r').readlines()
    #     classnames = [c.strip() for c in contentc]
    #     contents = open(file_name, 'r').readlines()
    #     random.shuffle(contents)
    #     classes = [[] for _ in classnames]
    #     imgs = [set() for _ in classnames]
    #     all_idxes = [i for i in range(len(contents))]
    #     for k,content in enumerate(contents):
    #         s = content.strip().split(' ')
    #         imgpath = s[0]
    #         s = s[1:]
    #         box_cnt = len(s) // 5
    #         osidx = ''
    #         for i in range(box_cnt):
    #             classes[i].append(s[i * 5])
    #             imgs[i].add(k)
    #
    #     size = len(content)
    #     train_size = round(size * train_rate)
    #     print('size:{},train:{},val:{}'.format(size, train_size, size - train_size))
    #     with open(out_train, 'w') as f:
    #         for line in content[:train_size]:
    #             f.write(line)
    #     with open(out_val, 'w') as f:
    #         for line in content[train_size:]:
    #             f.write(line)

    @staticmethod
    def data_draw_annotxt(annotation_path, classname_txt, save_dir):
        content = open(classname_txt, 'r').readlines()
        classnames = [c.strip() for c in content]
        color_table = get_color_table(len(classnames))
        anno = open(annotation_path, 'r')
        for line in anno:
            s = line.strip().split(' ')
            imgpath = s[0]
            dst = os.path.join(save_dir, os.path.basename(imgpath))
            s = s[1:]
            box_cnt = len(s) // 5
            box_names = []
            for i in range(box_cnt):
                x_min, y_min, x_max, y_max = float(s[i * 5 + 1]), float(s[i * 5 + 2]), float(s[i * 5 + 3]), float(
                    s[i * 5 + 4])
                idx = int(s[i * 5])
                box_names.append([x_min, y_min, x_max, y_max, classnames[idx]])
            if len(box_names) == 0:
                continue
            save_labeled_img(imgpath, box_names, dst, classnames, color_table=color_table)
            print(imgpath, " is saved.")

    @staticmethod
    def data_generate(train_txt, do_flip1=True, do_rot90=True, do_crop=True):
        datagene = dataGenerater(train_txt)
        datagene.generate(do_flip1=do_flip1, do_rot90=do_rot90,do_crop=do_crop)

    @staticmethod
    def relabel_(annotation_path, out_classnames_path, out_anno_path, eclassindexes, classnames):
        # eclassindexes:classnames的第一个类名对应的那些类别索引如[0,3,4]对应firebox
        # eclassindexes=[[],[],[],...]，classnames=['firebox', 'fire',...]
        class_picsnum = [0 for _ in range(len(classnames))]
        anno = open(annotation_path, 'r')
        danno = open(out_anno_path, 'w')
        for line in anno:
            flag = 0
            s = line.strip().split(' ')
            dline = s[0]
            s = s[1:]
            box_cnt = len(s) // 5
            for i in range(box_cnt):
                x_min, y_min, x_max, y_max = float(s[i * 5 + 1]), float(s[i * 5 + 2]), float(s[i * 5 + 3]), float(
                    s[i * 5 + 4])
                idx = int(s[i * 5])
                for k in range(len(eclassindexes)):
                    if idx in eclassindexes[k]:
                        dline = dline + ' ' + str(k) + ' ' + str(x_min) + ' ' + str(y_min) + ' ' + str(x_max) + ' ' + str(
                            y_max)
                        flag = 1
                        class_picsnum[k]+=1
                        break
            if flag == 0:
                continue
            danno.write(dline)
            danno.write('\n')
        danno.close()
        anno.close()
        print('class_picsnum:',class_picsnum)
        cf = open(out_classnames_path, 'w')
        for name in classnames:
            cf.write(name)
            cf.write('\n')
        cf.close()

    @staticmethod
    def send_class_dirs(annotation_path, classnames_path, dst_dir, choose_idx=[]):
        content = open(classnames_path, 'r').readlines()
        classnames = [c.strip() for c in content]
        if len(choose_idx) == 0:
            choose_idx = [i for i in range(len(classnames))]
        # newdir = os.path.join(dst_dir, str(110))
        # os.mkdir(newdir)
        for i in choose_idx:
            newdir = os.path.join(dst_dir, classnames[i])
            os.mkdir(newdir)
        anno = open(annotation_path, 'r')
        for line in anno:
            s = line.strip().split(' ')
            imgpath = s[0]

            s = s[1:]
            box_cnt = len(s) // 5

            osidx = ''
            for i in range(box_cnt):
                if osidx == '':
                    if s[i * 5] in choose_idx:
                        osidx=s[i * 5]
                    continue
                # if s[i * 5] != osidx:
                #     osidx= '110'
            if osidx == '':
                print('more than 1 or no label:', imgpath)
                continue
            dst = os.path.join(dst_dir, classnames[osidx])
            shutil.copy(imgpath, dst)

    @staticmethod
    def class_distribute(annotation_path, classnames):
        class_sum = [0 for _ in range(len(classnames))]
        anno = open(annotation_path, 'r')
        for line in anno:
            flag = 0
            s = line.strip().split(' ')
            dline = s[0]
            s = s[1:]
            box_cnt = len(s) // 5
            for i in range(box_cnt):
                # x_min, y_min, x_max, y_max = float(s[i * 5 + 1]), float(s[i * 5 + 2]), float(s[i * 5 + 3]), float(
                #     s[i * 5 + 4])
                idx = int(s[i * 5])
                class_sum[idx]+=1
        anno.close()
        print('class_picsnum:', class_sum)


if __name__ == '__main__':
    data_dir = './data'
    dp = dataProcess(data_dir)
    dp.run(do_json2txt=True)
    #dp.run(do_data_generate=True)
    #adjust val:train_rate    = train/whole           now is 0.9
    #dp.run(do_seperate_trainval=True)