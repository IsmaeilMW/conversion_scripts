"""coco2Yolo.py: Converts MS COCO annotation files to
                  YOLO format bounding box label files
__author__ = "Mohammad Ismaeil"
"""

import os
from pycocotools.coco import COCO
import shutil
import cv2
import tqdm
import yaml
from pathlib import Path


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


def coco2yolo(cat_names, ann_files, img_files, r_height_width, save_dir):
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
            if o_height_width[0] == r_height_width[0]:
                copy_files(img_files / img_fname, save_dir / img_fname)
            else:
                resize_flag = True
                img = cv2.imread(Path(img_files).as_posix() + '/' + img_fname)
                resize_img = resize_image(img, r_height_width)
                cv2.imwrite(Path(save_dir).as_posix() + '/' + img_fname, resize_img)

            # open text file
            with open(Path(save_dir).as_posix() + '/' + img_fname.split('.')[0] + '.txt', 'w') as label_file:
                anns = coco.loadAnns(ann_ids)
                for a in anns:
                    bbox = a['bbox']
                    bbox = [abs(coord) for coord in bbox]
                    if resize_flag:
                        bbox = resize_annotation_data(bbox, r_height_width, o_height_width)

                    # Convert COCO bbox coords to yolo ones
                    centre_x, centre_y = bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2
                    bbox = [centre_x / r_height_width[1], centre_y / r_height_width[0],
                            bbox[2] / r_height_width[1], bbox[3] / r_height_width[0]]
                    bbox = [str(b) for b in bbox]
                    cat_name = cat_idx[a['category_id']]
                    split_cat_name = cat_name.split('_')
                    if split_cat_name[-1] in ['connected', 'disconnected']:
                        cat_name = '_'.join(split_cat_name[:-1])
                    cat_id = sel_catNms.index(cat_name)
                    # Format line in label file
                    # Note: all whitespace will be removed from class names
                    out_str = [str(cat_id)
                               + ' ' + ' '.join([b for b in bbox])
                               + '\n']
                    label_file.write(out_str[0])


if __name__ == '__main__':
    with open('params.yaml') as f:
        my_dict = yaml.safe_load(f)
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]
    dataset_dir = my_dict['training']['save_dir']
    root_dir = ROOT / dataset_dir
    
    dataset_list = my_dict['training']['dataset_list']
    output_dir = root_dir / 'detection/yolo/'
    req_height = my_dict['training']['req_height']
    req_width = my_dict['training']['req_width']

    # Check if old file exits.
    if os.path.exists(output_dir):
        # dir_list = os.listdir(output_dir)
        # if len(dir_list) > 0:
        #     for dir_name in dir_list:
        #         shutil.rmtree(os.getcwd() + '/model_data/separated_data/data_1/yolo/' + dir_name)
        pass
    else:
        os.mkdir(output_dir)

    event_cat = my_dict['training']['labels']['event_cat']
    non_event_cat = my_dict['training']['labels']['non_event_cat']
    sel_catNms = my_dict['training']['labels']['sel_catNms']
    
    for d_set in tqdm.tqdm(dataset_list):
        annFile = Path(root_dir).as_posix() + '/coco/%s/dataset.json' % d_set
        imgFile = root_dir / d_set
        if os.path.isdir(output_dir / d_set):
            print('Labels folder already exists - exiting to prevent badness')
        else:
            os.mkdir(output_dir / d_set)
            coco2yolo(sel_catNms, annFile, imgFile, [req_height, req_width], output_dir / d_set)
