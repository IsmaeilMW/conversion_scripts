"""
This file is responsible for
adding multiple obj annotation into one file.
e.g.
directory name      obj annotated
annotation_1        airplane, jet bridge, pushback tug
annotation_2        chocks, fueling truck

output :
combine_1_2         airplane, jet bridge, pushback tug, chocks, fueling truck
"""
import json
import os
import shutil
import tqdm


class MergeAnnData:
    def __init__(self, input_loc, output_loc):
        self.input_loc = input_loc
        self.output_loc = output_loc

    @staticmethod
    def create_directory(save_dir):
        if os.path.exists(save_dir):
            pass
        else:
            os.mkdir(save_dir)

    def change_img_path(self, video_dir, ann_dir):
        self.create_directory(self.output_loc + '/' + video_dir + '/' + ann_dir + 'm_img_path')
        file_list = os.listdir(self.input_loc + '/' + video_dir + '/' + ann_dir)
        for file in tqdm.tqdm(file_list):
            if file.endswith('.json'):
                with open(self.input_loc + '/' + video_dir + '/' + ann_dir + '/' + file, 'r') as json_file:
                    json_data = json.load(json_file)

                    img_path = json_data['imagePath']
                    img_path = '../../' + img_path
                    json_data['imagePath'] = img_path

                with open(self.output_loc + '/' + video_dir + '/' + ann_dir + 'm_img_path' + '/' + file, 'w') as save_file:
                    json.dump(json_data, save_file)

    def combine_json_data(self, video_dir, ann_master, ann_slave, output_loc, file_name):
        with open(self.input_loc + '/' + video_dir + '/' + ann_master + '/' + file_name, 'r') as json_file:
            json_data_m = json.load(json_file)
            # print(json_data_m)
        with open(self.input_loc + '/' + video_dir + '/' + ann_slave + '/' + file_name, 'r') as json_file:
            json_data_s = json.load(json_file)
            # print(json_data_s)
            for idx, annotation in enumerate(json_data_s['shapes']):
                json_data_m['shapes'].append(annotation)

        with open(self.output_loc + '/' + video_dir + '/' + output_loc + '/' + file_name, 'w') as save_file:
            json.dump(json_data_m, save_file)

    def merge_data(self, video_dir, ann_master, ann_slave):
        a_m, a_n = ann_master.split('_')[-1], ann_slave.split('_')[-1]
        combine_dir_name = 'combine' + '_' + a_m + '_' + a_n
        self.create_directory(self.output_loc + '/' + video_dir + '/' + combine_dir_name)
        for ann_dir in [ann_master, ann_master]:
            if not os.path.exists(self.input_loc + '/' + video_dir + '/' + ann_dir):
                return ValueError(f"{ann_dir} does not exits")

        file_list_m = os.listdir(self.input_loc + '/' + video_dir + '/' + ann_master)
        for file_m in tqdm.tqdm(file_list_m):
            if file_m.endswith('.json'):
                self.combine_json_data(video_dir, ann_master, ann_slave, combine_dir_name, file_m)


if __name__ == '__main__':
    os.chdir(r"..\\")
    input_dir = os.getcwd() + '/annotation/verified'
    output_dir = os.getcwd() + '/annotation/verified'
    merge_data = MergeAnnData(input_dir, output_dir)
    merge_data.merge_data('video_5', 'annotation_1', 'annotation_2')
    # merge_data.change_img_path('video_6', 'annotation_1')
