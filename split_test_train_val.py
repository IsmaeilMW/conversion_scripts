import json
import os
import shutil
import tqdm


def copy_data(input_loc, output_loc, json_or_img):
    if json_or_img == 'json':
        change_path_in_json(input_loc, output_loc)
    else:
        shutil.copy2(input_loc, output_loc)


def move_files(source_file, des_file):
    os.rename(source_file, des_file)


def change_path_in_json(json_path, save_dir):
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
        file_name = json_path.split('/')[-1]
        img_path = file_name.split('.')[0] + '.jpg'
        json_data['imagePath'] = img_path

        if 'imageData' in json_data:
            json_data['imageData'] = None
    with open(save_dir + '/' + file_name, 'w') as save_file:
        json.dump(json_data, save_file)


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
                move_files(in_image_dir + '/' + file_name, save_dir + 'test' + '/' + file_name)
                copy_data(in_annotation_dir + '/' + ann_file_name, save_dir + 'test', 'json')

                # copy_data(in_image_dir + '/' + file_name, save_dir + 'test', 'img')
                test_count += 1
            elif test_count > val_count:
                move_files(in_image_dir + '/' + file_name, save_dir + 'val' + '/' + file_name)
                copy_data(in_annotation_dir + '/' + ann_file_name, save_dir + 'val', 'json')

                # copy_data(in_image_dir + '/' + file_name, save_dir + 'val', 'img')
                val_count += 1

        else:
            move_files(in_image_dir + '/' + file_name, save_dir + 'train' '/' + file_name)
            copy_data(in_annotation_dir + '/' + ann_file_name, save_dir + 'train', 'json')

            # copy_data(in_image_dir + '/' + file_name, save_dir + 'train', 'img')

        count += 1


if __name__ == '__main__':
    if os.name == 'nt':
        os.chdir(r"..\\")
    else:
        os.chdir(r"../")
    dataset_dir = '4'

    input_image_dir = os.getcwd() + '/model_data/datasets/' + dataset_dir + '/merge_files/images'
    input_annotation_dir = os.getcwd() + '/model_data/datasets/' + dataset_dir + '/merge_files/annotation'
    output_dir = os.getcwd() + '/model_data/datasets/' + dataset_dir + '/'
    create_test_train_val(input_image_dir, input_annotation_dir, output_dir)
