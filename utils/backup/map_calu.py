# coding: utf-8
import numpy as np

class mAP:
    labels_num = 0
    score_threshs = np.arange(0.0, 1.05, 0.05)
    # score_threshs = [i for i in range(10)]
    ap_params = []  #  [{ap_label},{ap_label}]

    def __init__(self, labels_num):
        self.labels_num = labels_num
        for i in range(np.size(self.score_threshs)):
            ap_label = {}
            ap_label['tp'] = [0 for _ in range(self.labels_num)]
            ap_label['fp'] = [0 for _ in range(self.labels_num)]
            ap_label['gt_num'] = [0 for _ in range(self.labels_num)]
            self.ap_params.append(ap_label)


    def add_APParams(self, predicts, groundtruth):
        # [[x1,y1,x2,y2,label,score],...]
        for i in range(np.size(self.score_threshs)):
            if np.size(predicts)==0:
                index = []
            else:
                index = np.where(predicts[:, 5] >= self.score_threshs[i])
            for label in range(self.labels_num):
                if np.size(index) == 0:
                    pre = []
                else:
                    pre = predicts[np.where(predicts[index][:, 4] == label)]  # [[x1, y1, x2, y2, score], ...]
                gt = groundtruth[np.where(groundtruth[:, 4] == label)]
                tp, fp, gt_num = self.__get_APparams_part(pre, gt, iou_thresh=0.65)
                self.ap_params[i]['tp'][label] += tp
                self.ap_params[i]['fp'][label] += fp
                self.ap_params[i]['gt_num'][label] += gt_num

    def save_pr_plt(self, savepath, plt_title='pr line'):
        precisions, recalls = self.__get_precision_recall()
        import matplotlib.pyplot as plt
        plt.figure()
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.plot(recalls, precisions, 'o-',label=u"线条")
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.title(plt_title)
        plt.savefig(savepath)
        plt.show()
        return

    def __get_APparams_part(self, pre, gt, iou_thresh=0.6):
        tp = 0
        fp = 0

        if np.size(gt) == 0 and np.size(pre)==0:
            return 0,0,0
        if np.size(gt) == 0:
            return 0, pre.shape[0], 0
        gt_num = gt.shape[0]
        if np.size(pre)==0:
            return tp,fp,gt_num

        for i in range(pre.shape[0]):
            flag = 0
            for j in range(gt_num):
                iou = self.getIOU(pre[i], gt[j])
                if iou > iou_thresh:
                    tp += 1
                    flag = 1
                    # gt[j]=[0,0,0,0,0]
                    break
            if flag==0:
                fp += 1
        # precision = tp/(tp+fp)
        # recall = tp/gt_num
        return tp, fp, gt_num


    def __get_precision_recall(self):
        precisions = []
        recalls = []
        for i in range(np.size(self.score_threshs)):
            precision_label = []
            recall_label = []
            print('score_thresh:{}'.format(self.score_threshs[i]))
            for label in range(self.labels_num):
                tp = self.ap_params[i]['tp'][label]
                fp = self.ap_params[i]['fp'][label]
                gt_num = self.ap_params[i]['gt_num'][label]
                p_temp = 1
                if tp+fp == 0:
                    precision_label.append(p_temp)
                else:
                    precision_label.append(tp/(tp+fp))
                    p_temp = tp/(tp+fp)
                recall_label.append(tp / (gt_num+0.000001))
                print('--label:{},precision:{},recall:{:.2f}'.format(label,p_temp,tp / (gt_num+0.000001)))
            recall_score = np.mean(np.array(recall_label))
            recalls.append(recall_score)
            precision_score = np.mean(np.array(precision_label))
            precisions.append(precision_score)
            print('--**--score_thresh:{} AVG:precision:{},recall:{}--**--'.format(self.score_threshs[i], precision_score, recall_score))
        return precisions,recalls

    def __precision_calc(self):
        precisions = []
        for i in range(np.size(self.score_threshs)):
            precision_label = []
            for label in range(self.labels_num):
                tp = self.ap_params[i]['tp'][label]
                fp = self.ap_params[i]['fp'][label]
                # gt_num = self.ap_params[i]['gt_num'][label]
                precision_label.append(tp/(tp+fp))
            precision_score = np.mean(np.array(precision_label))
            precisions.append(precision_score)
        return precisions

    def __recall_calc(self):
        recalls = []
        for i in range(np.size(self.score_threshs)):
            recall_label = []
            for label in range(self.labels_num):
                tp = self.ap_params[i]['tp'][label]
                # fp = self.ap_params[i]['fp'][label]
                gt_num = self.ap_params[i]['gt_num'][label]
                recall_label.append(tp/gt_num)
            recall_score = np.mean(np.array(recall_label))
            recalls.append(recall_score)
        return recalls

    @staticmethod
    def getIOU(box1,box2):  # [[x1, y1, x2, y2,?], ...]
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        xx1 = np.maximum(box1[0], box2[0])
        yy1 = np.maximum(box1[1], box2[1])
        xx2 = np.minimum(box1[2], box2[2])
        yy2 = np.minimum(box1[3], box2[3])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        # ovr = inter / (area1 + area2 - inter)
        ovr = inter / area2
        return ovr