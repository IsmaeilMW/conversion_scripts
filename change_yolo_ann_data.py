import os
import tqdm


def create_directory(save_dir):
    """images"""
    if os.path.exists(save_dir):
        # shutil.rmtree(save_dir + '/' + 'video_1_modified')
        # os.mkdir(save_dir + '/' + 'video_1_modified')
        pass
    else:
        os.mkdir(save_dir)


def change_yolo_data(data_dir_1, data_dir_2, save_dir):
    dir_list = os.listdir(data_dir_1)
    # dir_list = ['rac_g23_video_15']
    last_file_id, last_file_ext = '0', '.txt'
    first_file_id, first_file_ext = '0', '.txt'
    start_file_id = 0
    dir_name = 'rac_g23_v15'

    for d_list in dir_list:
        create_directory(save_dir + '/' + d_list)
        file_list = os.listdir(data_dir_1 + '/' + d_list)
        selected_files = []
        for file in file_list:
            if file.endswith('.txt'):
                name_split = file.split('_')
                merge_file_name = '_'.join(name_split[:-1])
                if merge_file_name == dir_name:
                    selected_files.append(file)
        for file in tqdm.tqdm(selected_files):
            with open(data_dir_1 + '/' + d_list + '/' + file, 'r') as input_data:
                data_to_add = input_data.readlines()
                input_data.close()
            with open(data_dir_2 + '/' + file, 'r') as merge_data:
                line_data = merge_data.readlines()
                line_data_m = []
                for data in line_data:
                    if data.startswith('4'):
                        pass
                    else:
                        line_data_m.append(data)
                merge_data.close()
            with open(save_dir + '/' + d_list + '/' + file, 'w') as updated_data:
                updated_data.writelines(line_data_m)
                updated_data.writelines(data_to_add)
                updated_data.close()


if __name__ == '__main__':
    os.chdir(r"..\\..\\")
    dataset_dir = '5'
    input_dir_1 = os.getcwd() + '/data/model_data/datasets/' + dataset_dir + '/' + 'detection/yolo'
    input_dir_2 = os.getcwd() + '/yolov5/runs/detect/exp28/labels'
    output_dir = input_dir_1 + '/' + 'updated'
    create_directory(output_dir)
    change_yolo_data(input_dir_1, input_dir_2, output_dir)
