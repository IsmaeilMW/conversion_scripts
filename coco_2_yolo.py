"""coco2Yolo.py: Converts MS COCO annotation files to
                  YOLO format bounding box label files
__author__ = "Mohammad Ismaeil"
"""

import os
from pycocotools.coco import COCO
import shutil


def coco2yolo(cat_names, ann_files, save_dir):
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
            # Get image filename
            img_fname = coco.imgs[img]['file_name']
            width = coco.imgs[img]['width']
            height = coco.imgs[img]['height']
            # open text file
            with open(save_dir + '/' + img_fname.split('.')[0] + '.txt', 'w') as label_file:
                anns = coco.loadAnns(ann_ids)
                for a in anns:
                    bbox = a['bbox']
                    # Convert COCO bbox coords to Kitti ones
                    centre_x, centre_y = (bbox[2] + bbox[0]) / 2, (bbox[3] + bbox[1]) / 2
                    bbox = [centre_x/width, centre_y/height, bbox[2]/width, bbox[3]/height]
                    bbox = [str(b) for b in bbox]
                    cat_name = cat_idx[a['category_id']]
                    # Format line in label file
                    # Note: all whitespace will be removed from class names
                    out_str = [cat_name.replace(" ", "")
                               + ' ' + ' '.join([b for b in bbox])
                               + '\n']
                    label_file.write(out_str[0])


if __name__ == '__main__':
    os.chdir(r"..\\")
    dataset_list = ['train', 'test', 'val']
    output_dir = os.getcwd() + '/model_data/separated_data/data_1/yolo/'

    # Check if old file exits.
    if os.path.exists(output_dir):
        # dir_list = os.listdir(output_dir)
        # if len(dir_list) > 0:
        #     for dir_name in dir_list:
        #         shutil.rmtree(os.getcwd() + '/model_data/separated_data/data_1/yolo/' + dir_name)
        pass
    else:
        os.mkdir(output_dir)

    # If this list is populated then label files will only be produced
    # for images containing the listed classes and only the listed classes
    # will be in the label file
    # catNms = ['person', 'dog', 'skateboard']
    # All cat names = ["cargo_loader", "jet_bridge", "belt_loader",
    #               "catering_vehicle", "cargo_door_opener_ladder", "pca", "airplane",
    #               "aircraft_front", "pushback_tug", "baggage", "tow_tractor", "chocks_on", "baggage_trailor",
    #               "chocks_off", "belt_loader_version2", "fwd_cargo_door_open"]
    sel_catNms = ["cargo_loader", "jet_bridge", "belt_loader",
                  "catering_vehicle", "pca",
                  "aircraft_front", "pushback_tug"]

    for d_set in dataset_list:
        # These settings assume this script is in the annotations directory
        # dataDir = 'model_data/image_w_ann/train'
        # segmentType = 'train'
        # annFile = '%s/annotations/instances_%s.json' % (dataDir, segmentType)
        annFile = 'model_data/separated_data/data_1/coco/%s/dataset.json' % d_set
        if os.path.isdir(output_dir + d_set):
            print('Labels folder already exists - exiting to prevent badness')
        else:
            os.mkdir(output_dir + d_set)
            coco2yolo(sel_catNms, annFile, output_dir + d_set)
