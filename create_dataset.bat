c:\venv\venv_RAC\Scripts\python.exe merge_files.py
echo merging_finished
c:\venv\venv_RAC\Scripts\python.exe split_test_train_val.py
echo created test train val
c:\venv\venv_RAC\Scripts\python.exe labelme_2_coco.py
echo generated labelme to coco data
c:\venv\venv_RAC\Scripts\python.exe generate_classification_data.py
echo generated classification data.
