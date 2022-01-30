"""coco2kitti.py: Converts MS COCO annotation files to
                  Kitti format bounding box label files
__author__ = "Jon Barker"
"""

import os
from pycocotools.coco import COCO


def coco2kitti(catNms, annFile):
    # initialize COCO api for instance annotations
    coco = COCO(annFile)

    # Create an index for the category names
    cats = coco.loadCats(coco.getCatIds())
    cat_idx = {}
    for c in cats:
        cat_idx[c['id']] = c['name']

    for img in coco.imgs:

        # Get all annotation IDs for the image
        catIds = coco.getCatIds(catNms=catNms)
        annIds = coco.getAnnIds(imgIds=[img], catIds=catIds)

        # If there are annotations, create a label file
        if len(annIds) > 0:
            # Get image filename
            img_fname = coco.imgs[img]['file_name']
            # open text file
            with open(save_dir + '/' + img_fname.split('.')[0] + '.txt', 'w') as label_file:
                anns = coco.loadAnns(annIds)
                for a in anns:
                    bbox = a['bbox']
                    # Convert COCO bbox coords to Kitti ones
                    bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
                    bbox = [str(b) for b in bbox]
                    catname = cat_idx[a['category_id']]
                    # Format line in label file
                    # Note: all whitespace will be removed from class names
                    out_str = [catname.replace(" ", "")
                               + ' ' + ' '.join(['0'] * 2)
                               + ' ' + ' '.join([b for b in bbox])
                               + ' ' + ' '.join(['0'] * 8)
                               + '\n']
                    label_file.write(out_str[0])


if __name__ == '__main__':
    os.chdir(r"..\\")

    # These settings assume this script is in the annotations directory
    dataDir = 'model_data/image_w_ann/train'
    segmentType = 'train'
    # annFile = '%s/annotations/instances_%s.json' % (dataDir, segmentType)
    annFile = 'model_data/coco/%s/dataset.json' % segmentType

    # If this list is populated then label files will only be produced
    # for images containing the listed classes and only the listed classes
    # will be in the label file
    # EXAMPLE:
    # catNms = ['person', 'dog', 'skateboard']
    catNms = ["cargo_loader_disconnected", "jet_bridge_connected", "belt_loader_disconnected",
              "catering_vehicle_connected", "cargo_door_opener_ladder", "pca_connected", "airplane",
              "aircraft_front"]

    # Check if a labels file exists and, if not, make one
    # If it exists already, exit to avoid overwriting
    save_dir = os.getcwd() + '/model_data/kitti/' + segmentType
    if os.path.isdir(save_dir):
        print('Labels folder already exists - exiting to prevent badness')
    else:
        os.mkdir(save_dir)
        coco2kitti(catNms, annFile)
