# coding: utf-8
# This script is modified from https://github.com/lars76/kmeans-anchor-boxes

from __future__ import division, print_function
from PIL import Image
from utils.data_utils import get_img
import numpy as np


def iou(box, clusters):
    """
    Calculates the Intersection over Union (IoU) between a box and k clusters.
    param:
        box: tuple or array, shifted to the origin (i. e. width and height)
        clusters: numpy array of shape (k, 2) where k is the number of clusters
    return:
        numpy array of shape (k, 0) where k is the number of clusters
    """
    x = np.minimum(clusters[:, 0], box[0])
    y = np.minimum(clusters[:, 1], box[1])
    if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
        raise ValueError("Box has no area")

    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[:, 0] * clusters[:, 1]

    iou_ = intersection / (box_area + cluster_area - intersection + 1e-10)

    return iou_


def avg_iou(boxes, clusters):
    """
    Calculates the average Intersection over Union (IoU) between a numpy array of boxes and k clusters.
    param:
        boxes: numpy array of shape (r, 2), where r is the number of rows
        clusters: numpy array of shape (k, 2) where k is the number of clusters
    return:
        average IoU as a single float
    """
    return np.mean([np.max(iou(boxes[i], clusters)) for i in range(boxes.shape[0])])


def translate_boxes(boxes):
    """
    Translates all the boxes to the origin.
    param:
        boxes: numpy array of shape (r, 4)
    return:
    numpy array of shape (r, 2)
    """
    new_boxes = boxes.copy()
    for row in range(new_boxes.shape[0]):
        new_boxes[row][2] = np.abs(new_boxes[row][2] - new_boxes[row][0])
        new_boxes[row][3] = np.abs(new_boxes[row][3] - new_boxes[row][1])
    return np.delete(new_boxes, [0, 1], axis=1)


def kmeans(boxes, k, dist=np.median):
    """
    Calculates k-means clustering with the Intersection over Union (IoU) metric.
    param:
        boxes: numpy array of shape (r, 2), where r is the number of rows
        k: number of clusters
        dist: distance function
    return:
        numpy array of shape (k, 2)
    """
    rows = boxes.shape[0]

    distances = np.empty((rows, k))
    last_clusters = np.zeros((rows,))

    np.random.seed()

    # the Forgy method will fail if the whole array contains the same rows
    clusters = boxes[np.random.choice(rows, k, replace=False)]

    while True:
        for row in range(rows):
            # print(row)
            distances[row] = 1 - iou(boxes[row], clusters)

        nearest_clusters = np.argmin(distances, axis=1)

        if (last_clusters == nearest_clusters).all():
            break

        for cluster in range(k):
            clusters[cluster] = dist(boxes[nearest_clusters == cluster], axis=0)

        last_clusters = nearest_clusters

    return clusters


def get_resizeBox(img, box, img_size):
    ori_height, ori_width = img.size[:2]
    # new_width, new_height = img_size
    # img_size = img_size0[0]
    # img_ori = Image.fromarray(img)
    # img_resized = letter_box_image(img_ori, img_size, img_size, 128)
    # img_resized = np.asarray(img_resized, np.float32)
    ratio = max(ori_height, ori_width) / img_size
    box = np.array(box) / ratio
    if ori_height > ori_width:
        box[0] += (img_size - ori_width / ratio) / 2
        box[2] += (img_size - ori_width / ratio) / 2
    elif ori_height < ori_width:
        box[1] += (img_size - ori_height / ratio) / 2
        box[3] += (img_size - ori_height / ratio) / 2
    return box

def parse_anno(annotation_path, img_size):
    anno = open(annotation_path, 'r',encoding='utf-8')
    result = []
    for line in anno:
        s = line.strip().split(' ')
        imgpath = s[0]
        print(imgpath)
        cimg = get_img(imgpath)

        img = Image.fromarray(cimg)
        # img = Image.open(imgpath)
        s = s[1:]
        box_cnt = len(s) // 5
        for i in range(box_cnt):
            x_min, y_min, x_max, y_max = float(s[i * 5 + 1]), float(s[i * 5 + 2]), float(s[i * 5 + 3]), float(
                s[i * 5 + 4])
            [x_min, y_min, x_max, y_max] = get_resizeBox(img, [x_min, y_min, x_max, y_max], img_size)
            width = x_max - x_min
            height = y_max - y_min
            # print(width,height)
            if width <= 0 or height <= 0:
                print('-----------------------', line)
            # assert width > 0
            # assert height > 0
            result.append([width, height])
    result = np.asarray(result)
    return result


def get_kmeans(anno, cluster_num=9):
    anchors = kmeans(anno, cluster_num)
    ave_iou = avg_iou(anno, anchors)

    anchors = anchors.astype('int').tolist()

    anchors = sorted(anchors, key=lambda x: x[0] * x[1])

    return anchors, ave_iou


def save_yolo_anchors(annotation_path, dst_path):
    anno_result = parse_anno(annotation_path, 416)  # [[w,h]...]
    anchors, ave_iou = get_kmeans(anno_result, 9)

    anchor_string = ''
    for anchor in anchors:
        anchor_string += '{},{}, '.format(anchor[0], anchor[1])
    anchor_string = anchor_string[:-2]

    print('anchors are:')
    print(anchor_string)
    print('the average iou is:')
    print(ave_iou)
    f = open(dst_path, 'w')
    f.write(anchor_string)
    f.close()


if __name__ == '__main__':
    #fdir = 'D:\\MyProgram\\标注工程\\project\\data\\all_label'
    fdir = './data/data_configs'
    annotation_path = fdir + "/Annotations.txt"
    dst_path = fdir + "/yolo_anchors.txt"
    save_yolo_anchors(annotation_path, dst_path)
