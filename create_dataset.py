import json
import os
import shutil
import tqdm

import cv2


def copy_data(input_loc, output_loc):
    shutil.copy2(input_loc, output_loc)


def create_directory(save_dir):
    if os.path.exists(save_dir):
        # shutil.rmtree(save_dir + '/' + 'video_1_modified')
        # os.mkdir(save_dir + '/' + 'video_1_modified')
        pass
    else:
        os.mkdir(save_dir)


def create_test_train_val(in_image_dir, in_annotation_dir, save_dir):
    file_list = os.listdir(in_image_dir)
    count = 0
    val_count = 0
    test_count = 0

    for dir_name in ['test', 'train', 'val']:
        create_directory(save_dir + '/' + dir_name)

    for file_name in tqdm.tqdm(file_list):
        split_file_name = file_name.split('.')
        ann_file_name = split_file_name[0] + '.json'
        if count % 10 == 0:
            if val_count >= test_count:
                # pass to validation
                copy_data(in_image_dir + '/' + file_name, save_dir + 'test')
                copy_data(in_annotation_dir + '/' + ann_file_name, save_dir + 'test')
                test_count += 1
            elif test_count > val_count:
                copy_data(in_image_dir + '/' + file_name, save_dir + 'val')
                copy_data(in_annotation_dir + '/' + ann_file_name, save_dir + 'val')
                val_count += 1

        else:
            copy_data(in_image_dir + '/' + file_name, save_dir + 'train')
            copy_data(in_annotation_dir + '/' + ann_file_name, save_dir + 'train')

        count += 1


if __name__ == '__main__':
    os.chdir(r"..\\")
    input_image_dir = os.getcwd() + '/model_data/separated_data/data_1/images/video_1'
    input_annotation_dir = os.getcwd() + '/model_data/separated_data/data_1/annotation/video_1'
    output_dir = os.getcwd() + '/model_data/separated_data/data_1/'
    create_test_train_val(input_image_dir, input_annotation_dir, output_dir)