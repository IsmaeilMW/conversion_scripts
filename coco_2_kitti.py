"""coco2kitti.py: Converts MS COCO annotation files to
                  Kitti format bounding box label files
__author__ = "Jon Barker"
"""

import os
from pycocotools.coco import COCO
import shutil
import tqdm
import cv2


def resize_image(img_file, height_width):
    resized_img = cv2.resize(img_file, (height_width[1], height_width[0]))
    return resized_img


def resize_annotation_data(ann_bbox, r_height_width, o_height_width):
    r_h, r_w = r_height_width
    o_h, o_w = o_height_width
    h_f, w_f = r_h / o_h, r_w / o_w
    bbox = ann_bbox[0] * w_f, ann_bbox[1] * h_f, ann_bbox[2] * w_f, ann_bbox[3] * h_f
    return bbox


def copy_files(source_file, des_file):
    shutil.copy2(source_file, des_file)


def coco2kitti(cat_names, ann_files, img_files, r_height_width, save_dir):
    # initialize COCO api for instance annotations
    resize_flag = False
    coco = COCO(ann_files)

    "Adding connected and disconnected on suffix of the event labels"
    cat_names_s = []
    for label_name in cat_names:
        if label_name in event_cat:
            cat_names_s.append(label_name + "_connected")
            cat_names_s.append(label_name + "_disconnected")
        else:
            cat_names_s.append(label_name)

    # Create an index for the category names
    cats = coco.loadCats(coco.getCatIds())
    cat_idx = {}
    for c in cats:
        cat_idx[c['id']] = c['name']

    for img in coco.imgs:

        # Get all annotation IDs for the image
        cat_ids = coco.getCatIds(catNms=cat_names_s)
        ann_ids = coco.getAnnIds(imgIds=[img], catIds=cat_ids)

        # If there are annotations, create a label file
        if len(ann_ids) > 0:
            # Get image filename
            img_fname = coco.imgs[img]['file_name']
            width = coco.imgs[img]['width']
            height = coco.imgs[img]['height']
            o_height_width = [height, width]

            "check whether resize is required"
            if o_height_width[0] == height:
                copy_files(img_files + '/' + img_fname, save_dir + '/images/' + img_fname)
            else:
                resize_flag = True
                img = cv2.imread(img_files + '/' + img_fname)
                resize_img = resize_image(img, r_height_width)
                cv2.imwrite(save_dir + '/images/' + img_fname, resize_img)

            # open text file
            with open(save_dir + '/labels/' + img_fname.split('.')[0] + '.txt', 'w') as label_file:
                anns = coco.loadAnns(ann_ids)
                for a in anns:
                    bbox = a['bbox']
                    bbox = [abs(coord) for coord in bbox]
                    if resize_flag:
                        bbox = resize_annotation_data(bbox, r_height_width, o_height_width)
                    # Convert COCO bbox coords to Kitti ones
                    bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
                    bbox = [str(b) for b in bbox]
                    cat_name = cat_idx[a['category_id']]
                    split_cat_name = cat_name.split('_')
                    if split_cat_name[-1] in ['connected', 'disconnected']:
                        cat_name = '_'.join(split_cat_name[:-1])
                    # Format line in label file
                    # Note: all whitespace will be removed from class names
                    out_str = [cat_name.replace(" ", "")
                               + ' ' + ' '.join(['0'] * 3)
                               + ' ' + ' '.join([b for b in bbox])
                               + ' ' + ' '.join(['0'] * 7)
                               + '\n']
                    label_file.write(out_str[0])


if __name__ == '__main__':
    if os.name == 'nt':
        os.chdir(r"..\\")
    else:
        os.chdir(r"../")
    dataset_list = ['train', 'test', 'val']
    output_dir = os.getcwd() + '/model_data/datasets/1/detection/kitti/'
    req_height = 720
    req_width = 1280

    # Check if old file exits.
    if os.path.exists(output_dir):
        # dir_list = os.listdir(output_dir)
        # if len(dir_list) > 0:
        #     for dir_name in dir_list:
        #         shutil.rmtree(os.getcwd() + '/model_data/separated_data/data_1/yolo/' + dir_name)
        pass
    else:
        os.mkdir(output_dir)

    event_cat = ["cargo_loader", "jet_bridge", "belt_loader", "catering_vehicle", "cargo_door_opener_ladder",
                 "pca", "pushback_tug"]
    non_event_cat = ["airplane", "aircraft_front", "pushback_tug", "baggage", "tow_tractor", "chocks_on",
                     "baggage_trailor", "chocks_off", "belt_loader_version2", "fwd_cargo_door_open"]
    sel_catNms = ["cargo_loader", "jet_bridge", "belt_loader",
                  "catering_vehicle", "pca",
                  "aircraft_front", "pushback_tug"]

    for d_set in tqdm.tqdm(dataset_list):
        annFile = os.getcwd() + '/model_data/datasets/1/coco/%s/dataset.json' % d_set
        imgFile = os.getcwd() + '/model_data/datasets/1/' + d_set
        if os.path.isdir(output_dir + d_set):
            print('Labels folder already exists - exiting to prevent badness')
        else:
            os.mkdir(output_dir + d_set)
            os.mkdir(output_dir + d_set + '/images')
            os.mkdir(output_dir + d_set + '/labels')
            coco2kitti(sel_catNms, annFile, imgFile, [req_height, req_width], output_dir + d_set)
