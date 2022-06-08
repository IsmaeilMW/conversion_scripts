import json
import os
import shutil
import tqdm
import yaml

import cv2
import logging


def change_json_data(json_path, save_dir, train_val, file_name):
    change_path_flag = True
    change_label_flag = False
    remove_labels_flag = False

    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
        # print(json_data)
        for idx, annotation in enumerate(json_data['shapes']):
            label_name = annotation['label']
            if change_label_flag:
                if label_name == "belt_loader_connected":
                    json_data['shapes'][idx]['label'] = "belt_loader_disconnected"
            elif remove_labels_flag:
                if label_name == "cargo_loader_connected":
                    json_data['shapes'].pop(idx)

        if change_path_flag:
            img_path = '../../../../images/' + train_val + '/' + file_name.split('.')[0] + '.jpg'

        json_data['imagePath'] = img_path

        if 'imageData' in json_data:
            json_data['imageData'] = None
    with open(save_dir + '/' + file_name, 'w') as save_file:
        json.dump(json_data, save_file)


def resize_images(img_path, save_dir, new_h_w, train_val, file_name):
    img = cv2.imread(img_path)
    if not img is None:
        resize_img = cv2.resize(img, [new_h_w[1], new_h_w[0]])
        cv2.imwrite(save_dir + '/' + train_val + '/' + file_name, resize_img)


def create_directory(save_dir):
    """images"""
    if os.path.exists(save_dir):
        # shutil.rmtree(save_dir + '/' + 'video_1_modified')
        # os.mkdir(save_dir + '/' + 'video_1_modified')
        pass
    else:
        os.mkdir(save_dir)


def resize_image_annotation(data_dir, save_dir, dir_list, ver_dir):
    last_file_id, last_file_ext = '0', '.json'
    first_file_id, first_file_ext = '0', '.json'
    start_file_id = 0

    for d_list in dir_list:
        create_directory(save_dir + '/' + d_list)
        # create_directory(save_dir + '/' + d_list + '/' + ver_dir)
        create_directory(save_dir + '/' + d_list + '/' + ver_dir + '_1')
        file_list = os.listdir(data_dir + '/' + d_list + '/' + ver_dir)
        # output_dir_files = os.listdir(save_dir + '/' + d_list + '/' + ver_dir)
        output_dir_files = os.listdir(save_dir + '/' + d_list + '/' + ver_dir + '_1')
        sorted_files = sorted(output_dir_files, reverse=True)
        if len(sorted_files) > 0:
            last_file_name = sorted_files[0]
            first_file_name = sorted_files[-1]
            last_file_id, last_file_ext = last_file_name.split('.')
            first_file_id, first_file_ext = first_file_name.split('.')
            # last_file_id = 1993
            # start_file_id = 724
        for file in tqdm.tqdm(file_list):
            if file.endswith('.json'):
                file_id, file_ext = file.split('.')
                if '_' in file_id:
                    file_id = file_id.split('_')[-1]
                if '_' in last_file_id:
                    last_file_id = last_file_id.split('_')[-1]
                if '_' in first_file_id:
                    first_file_id = first_file_id.split('_')[-1]
                # line change shift+Alt+ [up or down]
                # if start_file_id < int(file_id) <= last_file_id:
                if int(file_id) >= int(last_file_id):
                    file_path = os.path.join(data_dir + '/' + d_list + '/' + ver_dir + '/' + file)
                    # file_path = os.path.join(data_dir + '/' + d_list + '_modified' + '/' + file)
                    # change_json_data(file_path, save_dir + '/' + d_list + '/' + ver_dir, d_list, file)
                    change_json_data(file_path, save_dir + '/' + d_list + '/' + ver_dir + '_1', d_list, file)
                if int(file_id) < int(first_file_id):
                    file_path = os.path.join(data_dir + '/' + d_list + '/' + ver_dir + '/' + file)
                    # file_path = os.path.join(data_dir + '/' + d_list + '_modified' + '/' + file)
                    change_json_data(file_path, save_dir + '/' + d_list + '/' + ver_dir, d_list, file)
                else:
                    continue
            # else:
            #     file_path = os.path.join(data_dir + '/' + d_list + '/' + file)
            #     resize_images(file_path, save_dir + '/' + d_list + '_modified', new_h_w, d_list, file)


if __name__ == '__main__':
    with open('params.yaml') as f:
        my_dict = yaml.safe_load(f)
    os.chdir(r"..\\")
    input_dir = os.getcwd() + '/' + my_dict['annotation']['input_dir']
    output_dir = os.getcwd() + '/' + my_dict['annotation']['output_dir']
    change_files_dir = my_dict['annotation']['ann_data_correction']['video_files']
    version_dir = my_dict['annotation']['ann_data_correction']['ann_label_ver']
    resize_image_annotation(input_dir, output_dir, change_files_dir, version_dir)
