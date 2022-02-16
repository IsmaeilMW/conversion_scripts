import os
import shutil
import tqdm

os.chdir("..\\")


def create_dir(save_dir):
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
        os.mkdir(save_dir)
        os.mkdir(save_dir + '/' + 'images')
        os.mkdir(save_dir + '/' + 'annotation')
    else:
        os.mkdir(save_dir)
        os.mkdir(save_dir + '/' + 'images')
        os.mkdir(save_dir + '/' + 'annotation')


def copy_files(source_file, des_file):
    shutil.copy2(source_file, des_file)


def rename_and_copy_files(source_file, des_file):
    os.rename(source_file, des_file)


def merge_files(img_dir, ann_dir, save_dir):
    img_dir_list = os.listdir(img_dir)
    ann_dir_list = os.listdir(ann_dir)
    assert len(img_dir_list) == len(ann_dir_list)
    for ann_dir_name in tqdm.tqdm(ann_dir_list):
        split_dir_name = ann_dir_name.split('_')
        if split_dir_name[-1] == 'modified':
            img_dir_name = '_'.join(split_dir_name[:-1])
            dir_id = split_dir_name[-2]
        else:
            img_dir_name = ann_dir_name
            dir_id = split_dir_name[-1]
        ann_file_list = os.listdir(ann_dir + '/' + ann_dir_name)
        for ann_file_name in ann_file_list:
            current_file_id = ann_file_name.split('.')[0]
            img_file_name = current_file_id + '.jpg'
            src_img = img_dir + '/' + img_dir_name + '/' + img_file_name
            src_ann = ann_dir + '/' + ann_dir_name + '/' + ann_file_name
            if "_" in current_file_id:
                copy_files(src_img, save_dir + '/' + 'images/' + img_file_name)
                copy_files(src_ann, save_dir + '/' + 'annotation/' + ann_file_name)
            else:
                new_file_id = 'v' + dir_id + '_' + current_file_id
                img_file_name = new_file_id + '.jpg'
                ann_file_name = new_file_id + '.json'
                rename_and_copy_files(src_img, save_dir + '/' + 'images/' + img_file_name)
                rename_and_copy_files(src_ann, save_dir + '/' + 'annotation/' + ann_file_name)


if __name__ == '__main__':
    dataset_dir = '2'
    root_dir = os.getcwd() + '/model_data/datasets/' + dataset_dir
    output_dir = root_dir + '/merge_files'
    create_dir(output_dir)
    merge_files(root_dir + '/images', root_dir + '/annotation', output_dir)
