import cv2
import os
import matplotlib.pyplot as plt

# data_dir = '/home/ismaeil/work_linux/work/rac/model_training/face-mask-detection/kitti_dir/'
data_dir = '/home/ismaeil/work_linux/work/rac/model_training/detectnet_v2_model/KITTI_dataset/'
image_name = '165'


def main(image, bbox):
    cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 1)
    plt.imshow(image)
    plt.show()
    # cv2.imshow("img", image)
    # cv2.waitKey(0)


if __name__ == '__main__':
    img = cv2.imread(data_dir + 'training/image/' + image_name + '.jpg')
    label_file = open(data_dir + 'training/label/' + image_name + '.txt', 'r')
    with label_file as label:
        data_list = label.readlines()
        for data in data_list:
            data = data.split(' ')
            l_name, x1, y1, x2, y2 = data[0], int(data[4]), int(data[5]), int(data[6]), int(data[7])
            bbox_data = [x1, y1, x2, y2]
            main(img, bbox_data)
