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


def check_boundary():
    pass


def crop_image(img, bbox, cat_name):
    if 'connected' or 'disconnected' in cat_name:
        split_name = cat_name.split('_')[:-1]
        cat_name = '_'.join(split_name)

    buffer_pixel = 50
    bbox = [abs(x) for x in bbox]
    crop_img = None
    if cat_name == 'jet_bridge':
        # left shift the x1y1 coordinates.
        n_x1, n_y1 = bbox[0] - buffer_pixel, int(bbox[1] - 0.5 * buffer_pixel)
        x2, y2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
        crop_img = img[n_y1:y2, n_x1:x2]
    elif cat_name == 'cargo_loader':
        # right shift the x2y2 coordinates.
        n_y1 = bbox[1] - int(0.5 * buffer_pixel)
        x2, y2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
        n_x2, n_y2 = x2 + buffer_pixel, y2
        crop_img = img[n_y1:n_y2, bbox[0]:n_x2]
    elif cat_name == 'belt_loader':
        # right shift the x2y2 coordinates.
        x2, y2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
        n_x2, n_y2 = x2 + 2 * buffer_pixel, y2
        crop_img = img[bbox[1]:n_y2, bbox[0]:n_x2]
    elif cat_name == 'catering_vehicle':
        # right shift the x2y2 coordinates.
        x2, y2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
        n_x2, n_y2 = x2 + 2 * buffer_pixel, y2
        crop_img = img[bbox[1]:n_y2, bbox[0]:n_x2]
    elif cat_name == 'pca':
        # left shift the x1y1 coordinates.
        n_x1, n_y1 = bbox[0] - 2 * buffer_pixel, int(bbox[1] - 0.5 * buffer_pixel)
        x2, y2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
        crop_img = img[n_y1:y2, n_x1:x2]
    elif cat_name == 'pushback_tug':
        # up shift the y1 coordinates.
        x1, n_y1 = bbox[0], bbox[1] - 2 * buffer_pixel
        x2, y2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
        nx2 = int(x2 + 0.5 * buffer_pixel)
        crop_img = img[n_y1:y2, x1:nx2]
        # cv2.imshow("crop_img", crop_img)
        # cv2.waitKey(0)
    return crop_img


def coco2classification(cat_names, ann_files, input_img_dir, save_dir):
    # initialize COCO api for instance annotations
    coco = COCO(ann_files)

    # Create an index for the category names
    cats = coco.loadCats(coco.getCatIds())
    cat_idx = {}
    for c in cats:
        cat_idx[c['id']] = c['name']

    for img in coco.imgs:

        # Get all annotation IDs for the image
        cat_ids = coco.getCatIds(catNms=cat_names)
        ann_ids = coco.getAnnIds(imgIds=[img], catIds=cat_ids)

        # If there are annotations, create a label file
        if len(ann_ids) > 0:
            cat_img_count = np.zeros(len(sel_catNms), dtype=np.int16)
            # Get image filename
            file_name = coco.imgs[img]['file_name']
            input_img = cv2.imread(input_img_dir + '/' + file_name)
            width = coco.imgs[img]['width']
            height = coco.imgs[img]['height']
            annotations = coco.loadAnns(ann_ids)
            for a in tqdm.tqdm(annotations):
                bbox = a['bbox']
                cat_name = cat_idx[a['category_id']]
                sel_cat_idx = sel_catNms.index(cat_name)
                cat_img_count[sel_cat_idx] += 1
                if not os.path.exists(save_dir + '/' + cat_name):
                    os.mkdir(save_dir + '/' + cat_name)
                crop_img = crop_image(input_img, bbox, cat_name)
                if crop_img is None:
                    continue
                else:
                    split_file = file_name.split('.')
                    suffix_add = split_file[0] + '_' + str(cat_img_count[sel_cat_idx])
                    new_file_name = suffix_add + '.jpg'
                    cv2.imwrite(save_dir + '/' + cat_name + '/' + new_file_name, crop_img)


if __name__ == '__main__':
    if os.name == 'nt':
        os.chdir(r"..\\")
    else:
        os.chdir(r"../")

    dataset_list = ['train', 'test', 'val']
    output_dir = os.getcwd() + '/model_data/datasets/1/classification'

    # Check if old file exits.
    if os.path.exists(output_dir):
        pass
    else:
        os.mkdir(output_dir)

    # All cat names = ["cargo_loader", "jet_bridge", "belt_loader",
    #               "catering_vehicle", "cargo_door_opener_ladder", "pca", "airplane",
    #               "aircraft_front", "pushback_tug", "baggage", "tow_tractor", "chocks_on", "baggage_trailor",
    #               "chocks_off", "belt_loader_version2", "fwd_cargo_door_open"]
    sel_catNms = ["cargo_loader_connected", "jet_bridge_connected", "belt_loader_connected",
                  "catering_vehicle_connected", "pca_connected", "aircraft_front", "pushback_tug_connected",
                  "cargo_loader_disconnected", "jet_bridge_disconnected", "belt_loader_disconnected",
                  "catering_vehicle_disconnected", "pca_disconnected", "pushback_tug_disconnected"]

    for d_set in tqdm.tqdm(dataset_list):
        # annFile = '%s/annotations/instances_%s.json' % (dataDir, segmentType)
        annFile = 'model_data/datasets/1/coco/%s/dataset.json' % d_set
        img_dir = os.getcwd() + '/model_data/datasets/1/' + d_set
        if not os.path.exists(output_dir + '/' + d_set):
            os.mkdir(output_dir + '/' + d_set)
        coco2classification(sel_catNms, annFile, img_dir, output_dir + '/' + d_set)
