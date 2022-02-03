import json
import os
import shutil
import tqdm

import cv2


def resize_json(json_path, save_dir, new_h_w, train_val, file_name):
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
        # print(json_data)
        img_h = json_data['imageHeight']
        img_w = json_data['imageWidth']
        norm_h, norm_w = new_h_w[0]/img_h, new_h_w[1]/img_w
        for idx, annotation in enumerate(json_data['shapes']):
            points = annotation['points']
            new_points = []
            for coord in points:
                coord_x, coord_y = coord
                n_coord_x, n_coord_y = coord_x * norm_w, coord_y * norm_h
                new_points.append([n_coord_x, n_coord_y])
            json_data['shapes'][idx]['points'] = new_points
        # img_path = save_dir + '/' + train_val + '/' + file_name.split('.')[0] + '.jpg'
        if save_dir.split('/')[-1] == 'image_w_ann':
            img_path = file_name.split('.')[0] + '.jpg'
        else:
            img_path = '../../images/' + train_val + '/' + file_name.split('.')[0] + '.jpg'

        json_data['imagePath'] = img_path
        json_data['imageHeight'] = new_h_w[0]
        json_data['imageWidth'] = new_h_w[1]

        if 'imageData' in json_data:
            json_data['imageData'] = None
    with open(save_dir + '/' + train_val + '/' + file_name, 'w') as save_file:
        json.dump(json_data, save_file)


def resize_images(img_path, save_dir, new_h_w, train_val, file_name):
    img = cv2.imread(img_path)
    if not img is None:
        resize_img = cv2.resize(img, (new_h_w[1], new_h_w[0]))
        cv2.imwrite(save_dir + '/' + train_val + '/' + file_name, resize_img)


def create_directory(save_dir):
    """images"""
    if os.path.exists(save_dir + '/' + 'images'):
        shutil.rmtree(save_dir + '/' + 'images')
        os.mkdir(save_dir + '/' + 'images')
        os.mkdir(save_dir + '/' + 'images' + '/' + 'train')
        os.mkdir(save_dir + '/' + 'images' + '/' + 'test')
        os.mkdir(save_dir + '/' + 'images' + '/' + 'val')
    else:
        os.mkdir(save_dir + '/' + 'images')
        os.mkdir(save_dir + '/' + 'images' + '/' + 'train')
        os.mkdir(save_dir + '/' + 'images' + '/' + 'test')
        os.mkdir(save_dir + '/' + 'images' + '/' + 'val')

    """annotations"""
    if os.path.exists(save_dir + '/' + 'annotations'):
        shutil.rmtree(save_dir + '/' + 'annotations')
        os.mkdir(save_dir + '/' + 'annotations')
        os.mkdir(save_dir + '/' + 'annotations' + '/' + 'train')
        os.mkdir(save_dir + '/' + 'annotations' + '/' + 'test')
        os.mkdir(save_dir + '/' + 'annotations' + '/' + 'val')
    else:
        os.mkdir(save_dir + '/' + 'annotations')
        os.mkdir(save_dir + '/' + 'annotations' + '/' + 'train')
        os.mkdir(save_dir + '/' + 'annotations' + '/' + 'test')
        os.mkdir(save_dir + '/' + 'annotations' + '/' + 'val')

    """images_plus_annotations"""
    if os.path.exists(save_dir + '/' + 'image_w_ann'):
        shutil.rmtree(save_dir + '/' + 'image_w_ann')
        os.mkdir(save_dir + '/' + 'image_w_ann')
        os.mkdir(save_dir + '/' + 'image_w_ann' + '/' + 'train')
        os.mkdir(save_dir + '/' + 'image_w_ann' + '/' + 'test')
        os.mkdir(save_dir + '/' + 'image_w_ann' + '/' + 'val')
    else:
        os.mkdir(save_dir + '/' + 'image_w_ann')
        os.mkdir(save_dir + '/' + 'image_w_ann' + '/' + 'train')
        os.mkdir(save_dir + '/' + 'image_w_ann' + '/' + 'test')
        os.mkdir(save_dir + '/' + 'image_w_ann' + '/' + 'val')


def resize_image_annotation(data_dir, save_dir, new_h_w):
    dir_list = ['train', 'val', 'test']

    create_directory(save_dir)
    for d_list in dir_list:
        file_list = os.listdir(data_dir + '/' + d_list)
        for file in tqdm.tqdm(file_list):
            if file.endswith('.json'):
                file_path = os.path.join(data_dir + '/' + d_list + '/' + file)
                resize_json(file_path, save_dir + '/annotations', new_h_w, d_list, file)
                resize_json(file_path, save_dir + '/image_w_ann', new_h_w, d_list, file)
                pass
            else:
                file_path = os.path.join(data_dir + '/' + d_list + '/' + file)
                resize_images(file_path, save_dir + '/images', new_h_w, d_list, file)
                resize_images(file_path, save_dir + '/image_w_ann', new_h_w, d_list, file)


if __name__ == '__main__':
    os.chdir(r"..\\")
    input_dir = os.getcwd() + '/model_data/separated_data/data_1'
    output_dir = os.getcwd() + '/model_data/separated_data/data_1/resize_data'
    new_h, new_w = 720, 1280
    resize_image_annotation(input_dir, output_dir, [new_h, new_w])
