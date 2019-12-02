# coding: utf-8

from __future__ import division, print_function

import cv2
import random


def get_color_table(class_num, seed=50):
    random.seed(seed)
    color_table = {}
    for i in range(class_num):
        color_table[i] = [random.randint(0, 255) for _ in range(3)]
    return color_table


def box_out2in(w, h, box):
    box[0] = max(3, box[0])
    box[1] = max(8, box[1])
    box[2] = min(w-2, box[2])
    box[3] = min(h-2, box[3])
    return box


def plot_one_box(img, coord, label=None, color=None, line_thickness=None):
    '''
    coord: [x_min, y_min, x_max, y_max] format coordinates.
    img: img to plot on.
    label: str. The label name.
    color: int. color index.
    line_thickness: int. rectangle line thickness.
    '''
    tl = line_thickness or int(round(0.002 * max(img.shape[0:2])))  # line thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    h, w = img.shape[:2]
    coord = box_out2in(w, h, coord)
    c1, c2 = (int(coord[0]), int(coord[1])), (int(coord[2]), int(coord[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=float(tl) / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1)  # filled
        # cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 2), 0, float(tl) / 3, [0, 0, 0], thickness=tf, lineType=cv2.LINE_AA)
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, float(tl) / 3, [0, 0, 0], thickness=tf, lineType=cv2.LINE_AA)


def save_labeled_img(path, box_names, dst, classnames, color_table=None):
    if color_table is None:
        color_table = get_color_table(len(classnames))
    img_ori = cv2.imread(path)
    for i in range(len(box_names)):
        [x0, y0, x1, y1, classname] = box_names[i]
        index = classnames.index(classname)
        plot_one_box(img_ori, [x0, y0, x1, y1], label=classname, color=color_table[index])
    # cv2.imshow('Detection result', img_ori)
    if dst is not None:
        cv2.imwrite(dst, img_ori)


def save_labeled_score_img(img_ori, box_label_scores, dst, classnames, color_table=None):
    if color_table is None:
        color_table = get_color_table(len(classnames))
    for i in range(len(box_label_scores)):
        [x0, y0, x1, y1, label, score] = box_label_scores[i]
        plot_one_box(img_ori, [x0, y0, x1, y1], label=classnames[label]+'{:.3}'.format(score), color=color_table[label])
    # cv2.imshow('Detection result', img_ori)
    # cv2.waitKey(0)
    if dst is not None:
        cv2.imwrite(dst, img_ori)
