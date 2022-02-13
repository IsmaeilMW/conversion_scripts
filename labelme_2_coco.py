# import package
import labelme2coco
import os
import sys
import shutil

if os.name == 'nt':
    os.chdir(r"..\\")
else:
    os.chdir(r"../")

data_dir = os.getcwd() + "/model_data/datasets/1"
save_dir = os.getcwd() + "/model_data/datasets/1"

train_folder = data_dir + "/train"
list_train = os.listdir(train_folder)

val_folder = data_dir + "/val"
list_val = os.listdir(val_folder)

test_folder = data_dir + "/test"
list_test = os.listdir(test_folder)

# set path for coco json to be saved
export_dir = save_dir + "/coco"

if os.path.exists(export_dir):
    dir_file_list = os.listdir(export_dir)
    if len(dir_file_list) > 0:
        for file in dir_file_list:
            shutil.rmtree(export_dir + '/' + file)

save_json_path = export_dir + "/train"

labelme2coco.convert(train_folder, save_json_path)
save_json_path = export_dir + '/val'
labelme2coco.convert(val_folder, save_json_path)
save_json_path = export_dir + '/test'
labelme2coco.convert(test_folder, save_json_path)
