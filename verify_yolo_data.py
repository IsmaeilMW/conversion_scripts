import cv2
import json
import os

os.chdir("..\\..\\")
data_dir = '/yolov5/runs/detect/exp28/'
list_file = os.listdir(os.getcwd() + data_dir)


def check_on_image():
    # file_id = list_file[-1].split('.')[0]
    file_id = 'rac_g23_v15_000001'
    img = cv2.imread(os.getcwd() + data_dir + file_id + '.jpg')
    height, width = img.shape[:2]
    # height, width = 1080, 1920
    with open(os.getcwd() + data_dir + '/labels/' + file_id + '.txt', 'r') as label_file:
        lines = label_file.readlines()
        for label_data in lines:
            label_data = label_data.split(" ")
            cat_name = label_data[0]
            label_coord = [float(coord) for coord in label_data[1:]]
            bbox_data = label_coord[0] * width, label_coord[1] * height, label_coord[2] * width, label_coord[3] * height
            x1, y1 = bbox_data[0] - bbox_data[2]//2, bbox_data[1] - bbox_data[3]//2
            x2, y2 = x1 + bbox_data[2], y1 + bbox_data[3]
            rect_coord = [int(coord) for coord in [x1, y1, x2, y2]]
            img = cv2.rectangle(img, (rect_coord[0], rect_coord[1]), (rect_coord[2], rect_coord[3]), (0, 0, 0), 3)
            print(sel_catNms[int(cat_name)])
            cv2.imshow("img", img)
            cv2.waitKey(0)


if __name__ == '__main__':
    sel_catNms = ["cargo_loader", "jet_bridge", "belt_loader",
                  "catering_vehicle", "pca",
                  "airplane_front", "pushback_tug"]
    check_on_image()
