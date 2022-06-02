import json
import os
import tqdm
import pandas as pd
import numpy as np


label_list = {'name': [], 'count': []}


def count_annotation(json_path):
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)

        label_data = json_data['shapes']
        for label in label_data:
            label_name = label['label']
            if label_name in label_list['name']:
                idx = label_list['name'].index(label_name)
                label_list['count'][idx] += 1
            else:
                label_list['name'].append(label_name)
                label_list['count'].append(0)
                idx = len(label_list['name'])
                label_list['count'][idx - 1] += 1


def annotation_status(data_dir):
    dir_list = ['video_5/annotation_2']

    for d_list in dir_list:
        file_list = os.listdir(data_dir + '/' + d_list)
        for file in tqdm.tqdm(file_list):
            if file.endswith('.json'):
                file_path = os.path.join(data_dir + '/' + d_list + '/' + file)
                count_annotation(file_path)
    print("Total annotation: ", np.sum(label_list['count']))
    print(pd.DataFrame(label_list))


if __name__ == '__main__':
    os.chdir(r"..\\")
    input_dir = os.getcwd() + '/annotation/received'
    annotation_status(input_dir)
