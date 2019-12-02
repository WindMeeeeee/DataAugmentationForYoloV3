# encoding: utf-8
from utils.data_utils import get_img, parse_line
import os
import cv2
from utils.plot_utils import plot_one_box


class dataGenerater:
    annotation_txt = ''
    dst_txt = 'train_extended.txt'
    temp_txt1 = 'temp1.txt'
    temp_txt2 = 'temp2.txt'

    def __init__(self, iannotation_txt, idst_txt=None):
        self.annotation_txt = iannotation_txt
        dirname = os.path.dirname(iannotation_txt)
        if idst_txt is None:
            self.dst_txt = os.path.join(dirname, self.dst_txt)
        else:
            self.dst_txt = idst_txt
        self.temp_txt1 = os.path.join(dirname, self.temp_txt1)
        self.temp_txt2 = os.path.join(dirname, self.temp_txt2)
        pass

    def generate(self, do_flip1=True, do_rot90=True, do_crop=True):
        dst = self.dst_txt
        if do_rot90 and do_flip1 and do_crop:
            temp1 = self.temp_txt1
            temp2 = self.temp_txt2
            self.generate_flip1_txt(self.annotation_txt, temp1)
            self.generate_rot90_txt(temp1, temp2)
            self.generate_crop_txt(temp2, dst)
        elif do_flip1 and do_crop:
            temp1 = self.temp_txt1
            self.generate_flip1_txt(self.annotation_txt, temp1)
            self.generate_crop_txt(temp1, dst)
        elif do_rot90 and do_flip1:
            temp = self.temp_txt1
            self.generate_flip1_txt(self.annotation_txt, temp)
            self.generate_rot90_txt(temp, dst)
        elif do_flip1:
            self.generate_flip1_txt(self.annotation_txt, dst)
        elif do_rot90:
            self.generate_rot90_txt(self.annotation_txt, dst)
        elif do_crop:
            self.generate_crop_txt(self.annotation_txt, dst)

    def generate_flip1_txt(self, annotation_txt, txt_dst):
        contents = open(annotation_txt, 'r').readlines()
        dstfile = open(txt_dst, 'w')
        for line in contents:
            pic_path, boxes, labels = parse_line(line, is_str=True)
            img = get_img(pic_path)

            try:
                h, w, _ = img.shape
            except:
                print('wrong', pic_path)
                continue
            # fimg = cv2.flip(img, 1)
            img_dstdir, imgname = os.path.split(pic_path)
            savepath = os.path.join(img_dstdir, 'flip1_' + imgname)
            aline = savepath
            for i in range(len(labels)):
                b = boxes[i]
                x1, y1, x2, y2 = w - b[2], b[1], w - b[0], b[3]
                # plot_one_box(img, [b[0], b[1], b[2], b[3]], label='test')
                # cv2.imshow('ori', img)
                # plot_one_box(fimg, [x1, y1, x2, y2], label='test')
                # cv2.imshow('test', fimg)
                # cv2.waitKey(0)
                aline = aline + ' {} {} {} {} {}'.format(labels[i], x1, y1, x2, y2)
            dstfile.write(aline)
            dstfile.write('\n')
        dstfile.close()
        self.concat_txts(annotation_txt, txt_dst)

    def generate_rot90_txt(self, annotation_txt, txt_dst):
        contents = open(annotation_txt, 'r').readlines()
        dstfile = open(txt_dst, 'w')
        for line in contents:
            pic_path, boxes, labels = parse_line(line, is_str=True)
            img = get_img(pic_path)
            try:
                h, w, _ = img.shape
            except:
                print('wrong', pic_path)
                continue
            # rimg = np.rot90(img).copy()
            img_dstdir, imgname = os.path.split(pic_path)
            savepath = os.path.join(img_dstdir, 'rot90_' + imgname)
            aline = savepath
            for i in range(len(labels)):
                b = boxes[i]
                x1, y1, x2, y2 = b[1], w - b[2], b[3], w - b[0]
                aline = aline + ' {} {} {} {} {}'.format(labels[i], x1, y1, x2, y2)
                # plot_one_box(img, [b[0], b[1], b[2], b[3]], label='test')
                # cv2.imshow('ori', img)
                # plot_one_box(rimg, [x1, y1, x2, y2], label='test')
                # cv2.imshow('test', rimg)
                # cv2.waitKey(0)
                # aline = aline + ' ' + str(labels[i]) + ' ' + str(b[0]) + ' ' + str(b[1]) + ' ' + str(b[2]) + ' ' + str(b[3])
            dstfile.write(aline)
            dstfile.write('\n')
        dstfile.close()
        self.concat_txts(annotation_txt, txt_dst)


    def generate_crop_txt(self, annotation_txt, txt_dst):
        # crop center region
        contents = open(annotation_txt, 'r').readlines()
        dstfile = open(txt_dst, 'w')
        for line in contents:
            pic_path, boxes, labels = parse_line(line, is_str=True)
            img = get_img(pic_path)
            try:
                h, w, _ = img.shape
            except:
                print('wrong', pic_path)
                continue
            # rimg = np.rot90(img).copy()
            img_dstdir, imgname = os.path.split(pic_path)
            savepath = os.path.join(img_dstdir, 'crop_' + imgname)
            aline = savepath
            flag = 0
            if h > w:
                st = int(h/2-w/2)
                rimg = img[st:st+w, :, :]
                for i in range(len(labels)):
                    b = boxes[i]
                    x1, y1, x2, y2 = b[0], max(1,b[1]-st), b[2], min(b[3]-st,w-2)
                    if (y2-y1)/(b[3]-b[1])<0.2 or (y2-y1)/w<0.05:
                        continue
                    aline = aline + ' {} {} {} {} {}'.format(labels[i], x1, y1, x2, y2)
                    flag = 1
                    # plot_one_box(img, [b[0], b[1], b[2], b[3]], label='test')
                    # cv2.imshow('ori', img)
                #     plot_one_box(rimg, [x1, y1, x2, y2], label='test')
                # cv2.imshow('test', rimg)
                # cv2.waitKey(0)
                    # aline = aline + ' ' + str(labels[i]) + ' ' + str(b[0]) + ' ' + str(b[1]) + ' ' + str(b[2]) + ' ' + str(b[3])
            elif h < w:
                st=int(w / 2 - h / 2)
                rimg = img[:, st:st+h, :]
                for i in range(len(labels)):
                    b = boxes[i]
                    x1, y1, x2, y2 = max(1, b[0]-st), b[1], min(b[2]-st,h-2), b[3]
                    if (x2-x1)/(b[2]-b[0])<0.2 or (x2-x1)/h<0.05:
                        continue
                    aline = aline + ' {} {} {} {} {}'.format(labels[i], x1, y1, x2, y2)
                    flag = 1
                    # plot_one_box(img, [b[0], b[1], b[2], b[3]], label='test')
                    # cv2.imshow('ori', img)
                    # plot_one_box(rimg, [x1, y1, x2, y2], label='test')
                # cv2.imshow('test', rimg)
                # cv2.waitKey(0)
                    # aline = aline + ' ' + str(labels[i]) + ' ' + str(b[0]) + ' ' + str(b[1]) + ' ' + str(b[2]) + ' ' + str(b[3])
            else:
                print('no crop', pic_path)
                continue
            if flag==0:
                continue
            dstfile.write(aline)
            dstfile.write('\n')
        dstfile.close()
        self.concat_txts(annotation_txt, txt_dst)

    @staticmethod
    def concat_txts(ori_txt, dst_txt):
        # two txts, concat ori to dst
        contents = open(ori_txt, 'r').readlines()
        dstfile = open(dst_txt, 'a')

        if open(dst_txt, 'r').readlines()[-1][-1] != '\n':
            dstfile.write('\n')
        for content in contents:
            dstfile.write(content)
        dstfile.close()