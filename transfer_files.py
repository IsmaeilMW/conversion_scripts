import numpy as np
import os
import shutil
import tqdm


def create_directory(save_dir):
    """images"""
    if os.path.exists(save_dir):
        # shutil.rmtree(save_dir + '/' + 'video_1_modified')
        # os.mkdir(save_dir + '/' + 'video_1_modified')
        pass
    else:
        os.mkdir(save_dir)


def extract_annotation_files(ref_img_dir, input_ann):
    dir_list = ['video_1']

    for dir_name in dir_list:
        create_directory(ref_img_dir + '/' + 'annotation' + '/' + dir_name)
        img_list = os.listdir(ref_img_dir + '/' + 'images' + '/' + dir_name)
        for file_name in tqdm.tqdm(img_list):
            ann_file_name = file_name.split('.')[0] + '.json'
            shutil.copy2(input_ann + '/' + dir_name + '_modified' + '/' + ann_file_name,
                         ref_img_dir + '/' + 'annotation' + '/' + dir_name)


def extract_image_files(ref_data_dir, input_img_dir):
    dir_list = ['video_1']

    for dir_name in dir_list:
        create_directory(ref_data_dir + '/' + 'images' + '/' + dir_name)
        ann_list = os.listdir(ref_data_dir + '/' + 'annotation' + '/' + dir_name)
        for file_name in tqdm.tqdm(ann_list):
            img_file_name = file_name.split('.')[0] + '.jpg'
            shutil.copy2(input_img_dir + '/' + dir_name + '/' + img_file_name,
                         ref_data_dir + '/' + 'images' + '/' + dir_name)


if __name__ == '__main__':
    os.chdir("..\\")
    ref_file_dir = 'model_data/separated_data/data_1/'
    ann_file_dir = 'annotation/'
    img_file_dir = 'images/'
    extract_annotation_files(ref_file_dir, ann_file_dir)
    # extract_image_files(ref_file_dir, img_file_dir)
