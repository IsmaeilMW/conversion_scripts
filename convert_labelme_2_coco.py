# import package
import labelme2coco
import os
import sys

os.chdir(r"..\\")


train_folder = "model_data/image_w_ann/train"
list_train = os.listdir(train_folder)

# val_folder = "data/input_data/resized_data/image_w_ann/val"
# list_val = os.listdir(val_folder)
#
# test_folder = "data/input_data/resized_data/image_w_ann/test"
# list_test = os.listdir(test_folder)

# set path for coco json to be saved
export_dir = "model_data/coco"

save_json_path = export_dir + "/train"
labelme2coco.convert(train_folder, save_json_path)
# save_json_path = export_dir + '/val.json'
# labelme2coco.convert(val_folder, save_json_path)
# save_json_path = export_dir + '/test.json'
# labelme2coco.convert(test_folder, save_json_path)
