# import package
import labelme2coco
import os
import sys
import shutil
import yaml
from pathlib import Path

with open('params.yaml') as f:
    my_dict = yaml.safe_load(f)
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
dataset_dir = my_dict['training']['save_dir']

data_dir = Path(ROOT / dataset_dir).as_posix()
save_dir = ROOT / dataset_dir

train_folder = data_dir + '/' + "train"
list_train = os.listdir(train_folder)

val_folder = data_dir + '/' + "val"
list_val = os.listdir(val_folder)

test_folder = data_dir + '/' + "test"
list_test = os.listdir(test_folder)

# set path for coco json to be saved
export_dir = save_dir / "coco"

if os.path.exists(export_dir):
    dir_file_list = os.listdir(export_dir)
    if len(dir_file_list) > 0:
        for file in dir_file_list:
            shutil.rmtree(export_dir / file)

if os.name == 'nt':
    save_json_path = export_dir / "train"
    labelme2coco.convert(train_folder, save_json_path)
    save_json_path = export_dir / 'val'
    labelme2coco.convert(val_folder, save_json_path)
    save_json_path = export_dir / 'test'
    labelme2coco.convert(test_folder, save_json_path)
else:
    save_json_path = export_dir / "train.json"
    labelme2coco.convert(train_folder, save_json_path)
    save_json_path = export_dir / 'val.json'
    labelme2coco.convert(val_folder, save_json_path)
    save_json_path = export_dir / 'test.json'
    labelme2coco.convert(test_folder, save_json_path)
