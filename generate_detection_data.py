import json
import os
import shutil
import tqdm
import cv2


def change_2_det_label(json_path, save_dir, new_h_w, file_name):
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
        # print(json_data)
        img_h = json_data['imageHeight']
        img_w = json_data['imageWidth']
        norm_h, norm_w = new_h_w[0]/img_h, new_h_w[1]/img_w
        for idx, annotation in enumerate(json_data['shapes']):
            label_name = annotation['label']
            label_split = label_name.split('_')
            label_ext = label_split[-1]
            if label_ext in ['connected', 'disconnected']:
                l_name = label_split[:-1]
                new_label_name = "_".join(l_name)
                json_data['shapes'][idx]['label'] = new_label_name

        if 'imageData' in json_data:
            json_data['imageData'] = None
    with open(save_dir + '/' + file_name, 'w') as save_file:
        json.dump(json_data, save_file)


def generate_detection_label(data_dir, save_dir, new_h_w):
    dir_list = ['video_1']
    last_file_id, last_file_ext = 0, '.json'
    start_file_id = 0

    for d_list in dir_list:
        file_list = os.listdir(data_dir + '/' + d_list)
        for file in tqdm.tqdm(file_list):
            if file.endswith('.json'):
                # line change shift+Alt+ [up or down]
                file_path = os.path.join(data_dir + '/' + d_list + '/' + file)
                change_2_det_label(file_path, save_dir + '/' + d_list, new_h_w, file)


if __name__ == '__main__':
    os.chdir(r"..\\")
    input_dir = os.getcwd() + '/model_data/separated_data/data_1/annotation'
    output_dir = os.getcwd() + '/model_data/separated_data/data_1/annotation'
    new_h, new_w = 1080, 1920
    generate_detection_label(input_dir, output_dir, [new_h, new_w])
