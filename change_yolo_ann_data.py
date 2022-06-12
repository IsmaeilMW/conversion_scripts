import os
import tqdm
import yaml
from pathlib import Path


def create_directory(save_dir):
    """images"""
    if os.path.exists(save_dir):
        # shutil.rmtree(save_dir + '/' + 'video_1_modified')
        # os.mkdir(save_dir + '/' + 'video_1_modified')
        pass
    else:
        os.mkdir(save_dir)


def change_yolo_data(data_dir, lbl_change_dir, label_gen_dir, save_dir, change_label_id):
    dir_list = os.listdir(lbl_change_dir)
    dir_name = data_dir
    start_ids = [str(k) for k in change_label_id]
    start_ids = tuple(start_ids)

    for d_list in dir_list:
        create_directory(save_dir / d_list)
        file_list = os.listdir(lbl_change_dir / d_list)
        selected_files = []
        for file in file_list:
            if file.endswith('.txt'):
                name_split = file.split('_')
                merge_file_name = '_'.join(name_split[:-1])
                if merge_file_name == dir_name:
                    selected_files.append(file)
        for file in tqdm.tqdm(selected_files):
            with open(lbl_change_dir.as_posix() + '/' + d_list + '/' + file, 'r') as input_data:
                data_to_add = input_data.readlines()
                input_data.close()
            with open(label_gen_dir.as_posix() + '/' + file, 'r') as merge_data:
                line_data = merge_data.readlines()
                line_data_m = []
                for data in line_data:
                    if data.startswith(start_ids):
                        line_data_m.append(data)
                    else:
                        pass
                merge_data.close()
            with open(save_dir.as_posix() + '/' + d_list + '/' + file, 'w') as updated_data:
                updated_data.writelines(line_data_m)
                updated_data.writelines(data_to_add)
                updated_data.close()


if __name__ == '__main__':
    with open('params.yaml') as f:
        my_dict = yaml.safe_load(f)
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]
    dataset_dir = my_dict['training']['save_dir']
    root_dir = ROOT / dataset_dir
    image_dir = my_dict['annotation']['change_yolo_ann_data']['image_dir']
    label_master = root_dir / my_dict['annotation']['change_yolo_ann_data']['master_dir']
    label_slave = ROOT.parent / my_dict['annotation']['change_yolo_ann_data']['slave_dir']
    output_dir = root_dir / my_dict['annotation']['change_yolo_ann_data']['save_dir']
    change_labels_id = my_dict['annotation']['change_yolo_ann_data']['change_ann_id']
    create_directory(output_dir)
    change_yolo_data(image_dir, label_master, label_slave, output_dir, change_labels_id)
