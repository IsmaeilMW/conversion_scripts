"""
generate_classification_data.py: create image dataset for classification.
__author__ = "Mohammad Ismaeil"
"""

import os
from pycocotools.coco import COCO
import shutil
import cv2
import numpy as np
import tqdm
from utils.classification_utils import crop_classification_1

threshold_height = 64
threshold_width = 128


def check_boundary():
    pass


def resize_image(img, input_shape, letter_box=True):
    if letter_box:
        img_h, img_w, _ = img.shape
        new_h, new_w = input_shape[0], input_shape[1]
        offset_h, offset_w = 0, 0
        if (new_w / img_w) <= (new_h / img_h):
            new_h = int(img_h * new_w / img_w)
            offset_h = (input_shape[0] - new_h) // 2
        else:
            new_w = int(img_w * new_h / img_h)
            offset_w = (input_shape[1] - new_w) // 2
        resized = cv2.resize(img, (new_w, new_h))
        img = np.full((input_shape[0], input_shape[1], 3), 127, dtype=np.uint8)
        img[offset_h:(offset_h + new_h), offset_w:(offset_w + new_w), :] = resized
    else:
        img = cv2.resize(img, (224, 224))
    return img


def coco2classification(cat_names, ann_files, input_img_dir, save_dir):
    # initialize COCO api for instance annotations
    coco = COCO(ann_files)

    # Create an index for the category names
    cats = coco.loadCats(coco.getCatIds())
    cat_idx = {}
    for c in cats:
        cat_idx[c['id']] = c['name']

    for img in tqdm.tqdm(coco.imgs):

        # Get all annotation IDs for the image
        cat_ids = coco.getCatIds(catNms=cat_names)
        ann_ids = coco.getAnnIds(imgIds=[img], catIds=cat_ids)

        # If there are annotations, create a label file
        if len(ann_ids) > 0:
            cat_img_count = np.zeros(len(sel_catNms), dtype=np.int16)
            # Get image filename
            file_name = coco.imgs[img]['file_name']
            if os.name == 'nt':
                input_img = cv2.imread(input_img_dir + '/' + file_name)
            else:
                input_img = cv2.imread(file_name)
            width = coco.imgs[img]['width']
            height = coco.imgs[img]['height']
            annotations = coco.loadAnns(ann_ids)
            for a in annotations:
                bbox = a['bbox']
                cat_name = cat_idx[a['category_id']]
                sel_cat_idx = sel_catNms.index(cat_name)
                cat_img_count[sel_cat_idx] += 1
                if not os.path.exists(save_dir + '/' + cat_name):
                    os.mkdir(save_dir + '/' + cat_name)
                crop_img = crop_classification_1(input_img, bbox, cat_name)
                if crop_img is None:
                    continue
                else:
                    if crop_img.shape[0] < threshold_height or crop_img.shape[1] < threshold_width:
                        continue
                    # resized_img = resize_image(crop_img, [224, 224])
                    resized_img = crop_img.copy()
                    if os.name == 'nt':
                        split_file = file_name.split('.')
                        suffix_add = split_file[0] + '_' + str(cat_img_count[sel_cat_idx])
                        new_file_name = suffix_add + '.jpg'

                        cv2.imwrite(save_dir + '/' + cat_name + '/' + new_file_name, resized_img)
                    else:
                        split_file = file_name.split('/')
                        split_file = split_file[-1].split('.')
                        suffix_add = split_file[0] + '_' + str(cat_img_count[sel_cat_idx])
                        new_file_name = suffix_add + '.jpg'
                        cv2.imwrite(save_dir + '/' + cat_name + '/' + new_file_name, resized_img)


if __name__ == '__main__':
    if os.name == 'nt':
        os.chdir(r"..\\")
    else:
        os.chdir(r"../")

    dataset_list = ['train', 'test', 'val']
    dataset_dir = '3'
    output_dir = os.getcwd() + '/model_data/datasets/' + dataset_dir + '/classification'

    # Check if old file exits.
    if os.path.exists(output_dir):
        pass
    else:
        os.mkdir(output_dir)

    # All cat names = ["cargo_loader", "jet_bridge", "belt_loader",
    #               "catering_vehicle", "cargo_door_opener_ladder", "pca", "airplane",
    #               "aircraft_front", "pushback_tug", "baggage", "tow_tractor", "chocks_on", "baggage_trailor",
    #               "chocks_off", "belt_loader_version2", "fwd_cargo_door_open"]
    # sel_catNms = ["cargo_loader_connected", "jet_bridge_connected", "belt_loader_connected",
    #               "catering_vehicle_connected", "pca_connected", "pushback_tug_connected",
    #               "cargo_loader_disconnected", "jet_bridge_disconnected", "belt_loader_disconnected",
    #               "catering_vehicle_disconnected", "pca_disconnected", "pushback_tug_disconnected"]
    sel_catNms = ["catering_vehicle_connected", "jet_bridge_connected",
                  "catering_vehicle_disconnected", "jet_bridge_disconnected"]

    for d_set in tqdm.tqdm(dataset_list):
        # annFile = '%s/annotations/instances_%s.json' % (dataDir, segmentType)
        print(os.listdir(os.getcwd() + '/model_data/datasets/' + dataset_dir + '/coco'))
        if os.name == 'nt':
            annFile = os.getcwd() + '/model_data/datasets/' + dataset_dir + '/coco/%s/dataset.json' % d_set
        else:
            annFile = os.getcwd() + '/model_data/datasets/' + dataset_dir + '/coco/%s.json' % d_set

        img_dir = os.getcwd() + '/model_data/datasets/' + dataset_dir + '/' + d_set
        if not os.path.exists(output_dir + '/' + d_set):
            os.mkdir(output_dir + '/' + d_set)
        coco2classification(sel_catNms, annFile, img_dir, output_dir + '/' + d_set)
