# coding: utf-8

from __future__ import division, print_function
import numpy as np
import cv2


def parse_line(line, is_str=False):
    '''
    Given a line from the training/test txt file, return parsed
    pic_path, boxes info, and label info.
    return:
        pic_path: string.
        boxes: shape [N, 4], N is the ground truth count, elements in the second
            dimension are [x_min, y_min, x_max, y_max]
    '''
    # print(line)
    if is_str:
        s = line.strip().split(' ')
    else:
        s = str(line, encoding="utf8").strip().split(' ')
    # print(s)
    pic_path = s[0]
    s = s[1:]
    box_cnt = len(s) // 5
    boxes = []
    labels = []
    for i in range(box_cnt):
        label, x_min, y_min, x_max, y_max = int(s[i * 5]), float(s[i * 5 + 1]), float(s[i * 5 + 2]), float(
            s[i * 5 + 3]), float(s[i * 5 + 4])
        boxes.append([x_min, y_min, x_max, y_max])
        labels.append(label)
    boxes = np.asarray(boxes, np.float32)
    labels = np.asarray(labels, np.int64)
    return pic_path, boxes, labels


def resize_image_and_correct_boxes(img, boxes, img_size):
    # convert gray scale image to 3-channel fake RGB image
    if len(img) == 2:
        img = np.expand_dims(img, -1)
    ori_height, ori_width = img.shape[:2]
    new_width, new_height = img_size
    # shape to (new_height, new_width)
    img = cv2.resize(img, (new_width, new_height))
    # cv2.imshow('s', img)
    # cv2.waitKey(0)
    # convert to float
    img = np.asarray(img, np.float32)

    # boxes
    # xmin, xmax
    boxes[:, 0] = boxes[:, 0] / ori_width * new_width
    boxes[:, 2] = boxes[:, 2] / ori_width * new_width
    # ymin, ymax
    boxes[:, 1] = boxes[:, 1] / ori_height * new_height
    boxes[:, 3] = boxes[:, 3] / ori_height * new_height
    # print(boxes)
    return img, boxes


from PIL import Image
# from utils.utils import letter_box_image
def letter_box_image(image: Image.Image, output_height: int, output_width: int, fill_value)-> np.ndarray:
    """
    Fit image with final image with output_width and output_height.
    :param image: PILLOW Image object.
    :param output_height: width of the final image.
    :param output_width: height of the final image.
    :param fill_value: fill value for empty area. Can be uint8 or np.ndarray
    :return: numpy image fit within letterbox. dtype=uint8, shape=(output_height, output_width)
    """

    height_ratio = float(output_height)/image.size[1]
    width_ratio = float(output_width)/image.size[0]
    fit_ratio = min(width_ratio, height_ratio)
    fit_height = int(image.size[1] * fit_ratio)
    fit_width = int(image.size[0] * fit_ratio)
    fit_image = np.asarray(image.resize((fit_width, fit_height), resample=Image.BILINEAR))

    if isinstance(fill_value, int):
        fill_value = np.full(fit_image.shape[2], fill_value, fit_image.dtype)

    to_return = np.tile(fill_value, (output_height, output_width, 1))
    pad_top = int(0.5 * (output_height - fit_height))
    pad_left = int(0.5 * (output_width - fit_width))
    to_return[pad_top:pad_top+fit_height, pad_left:pad_left+fit_width] = fit_image
    return to_return



def resize_image_and_correct_boxes_fill(img, boxes, img_size0):
    # convert gray scale image to 3-channel fake RGB image
    if len(img) == 2:
        img = np.expand_dims(img, -1)
    ori_height, ori_width = img.shape[:2]
    # new_width, new_height = img_size
    img_size = img_size0[0]
    img_ori = Image.fromarray(img)
    img_resized = letter_box_image(img_ori, img_size, img_size, 128)
    img_resized = np.asarray(img_resized, np.float32)
    ratio = max(ori_height, ori_width) / img_size
    boxes = boxes / ratio
    try:
        if ori_height > ori_width:
            boxes[:, 0] += (img_size - ori_width / ratio) / 2
            boxes[:, 2] += (img_size - ori_width / ratio) / 2
        elif ori_height < ori_width:
            boxes[:, 1] += (img_size - ori_height / ratio) / 2
            boxes[:, 3] += (img_size - ori_height / ratio) / 2
    except:
        img_ori.save('wrong.jpg')
        print('wrong:h:{},w:{},box:{}'.format(ori_height, ori_width,boxes))
    return img_resized, boxes


def convert_to_original_box(box, ori_size, img_size):
    ori_height, ori_width = ori_size[:2]
    ratio = max(ori_height, ori_width) / img_size
    box = box * ratio
    if ori_height > ori_width:
        box[0] -= (img_size * ratio - ori_width) / 2
        box[2] -= (img_size * ratio - ori_width) / 2
    elif ori_height < ori_width:
        box[1] -= (img_size * ratio - ori_height) / 2
        box[3] -= (img_size * ratio - ori_height) / 2
    box[0] = max(0,box[0])
    box[1] = max(0, box[1])
    box[2] = min(ori_width, box[2])
    box[3] = min(ori_height, box[3])
    return box


def data_augmentation(img, boxes, label):
    '''
    Do your own data augmentation here.
    param:
        img: a [H, W, 3] shape RGB format image, float32 dtype
        boxes: [N, 4] shape boxes coordinate info, N is the ground truth box number,
            4 elements in the second dimension are [x_min, y_min, x_max, y_max], float32 dtype
        label: [N] shape labels, int64 dtype (you should not convert to int32)
    '''
    return img, boxes, label


def process_box(boxes, labels, img_size, class_num, anchors):
    '''
    Generate the y_true label, i.e. the ground truth feature_maps in 3 different scales.
    '''
    anchors_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]]

    # convert boxes form:
    # shape: [N, 2]
    # (x_center, y_center)
    box_centers = (boxes[:, 0:2] + boxes[:, 2:4]) / 2
    # (width, height)
    box_sizes = boxes[:, 2:4] - boxes[:, 0:2]

    # [13, 13, 3, 3+num_class]
    y_true_13 = np.zeros((img_size[1] // 32, img_size[0] // 32, 3, 5 + class_num), np.float32)
    y_true_26 = np.zeros((img_size[1] // 16, img_size[0] // 16, 3, 5 + class_num), np.float32)
    y_true_52 = np.zeros((img_size[1] // 8, img_size[0] // 8, 3, 5 + class_num), np.float32)

    y_true = [y_true_13, y_true_26, y_true_52]

    # [N, 1, 2]
    box_sizes = np.expand_dims(box_sizes, 1)
    # broadcast tricks
    # [N, 1, 2] & [9, 2] ==> [N, 9, 2]
    mins = np.maximum(- box_sizes / 2, - anchors / 2)
    maxs = np.minimum(box_sizes / 2, anchors / 2)
    # [N, 9, 2]
    whs = maxs - mins

    # [N, 9]
    iou = (whs[:, :, 0] * whs[:, :, 1]) / (
            box_sizes[:, :, 0] * box_sizes[:, :, 1] + anchors[:, 0] * anchors[:, 1] - whs[:, :, 0] * whs[:, :,
                                                                                                     1] + 1e-10)
    # [N]
    best_match_idx = np.argmax(iou, axis=1)

    ratio_dict = {1.: 8., 2.: 16., 3.: 32.}
    for i, idx in enumerate(best_match_idx):
        # idx: 0,1,2 ==> 2; 3,4,5 ==> 1; 6,7,8 ==> 2
        feature_map_group = 2 - idx // 3
        # scale ratio: 0,1,2 ==> 8; 3,4,5 ==> 16; 6,7,8 ==> 32
        ratio = ratio_dict[np.ceil((idx + 1) / 3.)]
        x = int(np.floor(box_centers[i, 0] / ratio))
        y = int(np.floor(box_centers[i, 1] / ratio))
        k = anchors_mask[feature_map_group].index(idx)
        c = labels[i]
        # print feature_map_group, '|', y,x,k,c
        # print()
        y_true[feature_map_group][y, x, k, :2] = box_centers[i]
        y_true[feature_map_group][y, x, k, 2:4] = box_sizes[i]
        y_true[feature_map_group][y, x, k, 4] = 1.
        y_true[feature_map_group][y, x, k, 5 + c] = 1.

    return y_true_13, y_true_26, y_true_52

import os
def get_img(pic_path):
    dir, img_name = os.path.split(pic_path)
    ss = img_name.split('_')
    path = os.path.join(dir, ss[-1])
    img = cv2.imread(path)
    for s in ss[::-1]:
        if s == 'flip1':
            img = cv2.flip(img, 1)
        elif s == 'rot90':
            img = np.rot90(img)
        elif s == 'crop':
            h, w, _ = img.shape
            if h > w:
                st = int(h / 2 - w / 2)
                img = img[st:st + w, :, :]
            else:
                st = int(w / 2 - h / 2)
                img = img[:, st:st + h, :]
            # cv2.imshow('x',img)
            # cv2.waitKey(0)
        else:
            continue
    return img


def parse_data(line, class_num, img_size, anchors, mode, reset_imgdir=None):
    '''
    param:
        line: a line from the training/test txt file
        args: args returned from the main program
        mode: 'train' or 'val'. When set to 'train', data_augmentation will be applied.
    '''
    pic_path, boxes, labels = parse_line(line)

    # img = cv2.imread(pic_path)
    if reset_imgdir is not None:
        #_, imgname = os.path.split(pic_path)
        imgname = pic_path.split('\\')[-1]
        pic_path = os.path.join(reset_imgdir.decode(), imgname)
    # print(pic_path)
    img = get_img(pic_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img, boxes = resize_image_and_correct_boxes_fill(img, boxes, img_size)

    # do data augmentation here
    if mode == 'train':
        img, boxes, labels = data_augmentation(img, boxes, labels)

    # the input of yolo_v3 should be in range 0~1
    img = img / 255.

    y_true_13, y_true_26, y_true_52 = process_box(boxes, labels, img_size, class_num, anchors)

    return img, y_true_13, y_true_26, y_true_52


def read_data_txt(data_file):
    imgpaths = []
    f = open(data_file, 'r')
    lines = f.readlines()
    for line in lines:
        temp = line.split(' ')
        imgpaths.append(temp[0])
    f.close()
    return imgpaths


def read_groundtruth_txt(data_file):
    imgpaths = []
    f = open(data_file, 'r')
    lines = f.readlines()
    groundtruths = []
    for line in lines:
        temp = line.split(' ')
        imgpaths.append(temp[0])
        s = temp[1:]
        box_num = len(s)//5
        if box_num ==0:
            groundtruths.append([])
            continue
        groundtruth = []
        for i in range(box_num):
            groundtruth.append([float(s[i*5+1]),float(s[i*5+2]),float(s[i*5+3]),float(s[i*5+4]),int(s[i*5])])
        groundtruths.append(groundtruth)
    f.close()
    return imgpaths,groundtruths
