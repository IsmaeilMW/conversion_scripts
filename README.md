#Order to follow
```
python transfer_files.py
----images
    ---video_fileid
----annotation
    ---video_fileid
---merge files
    python merge_files.py
---split files in test/train/val
    python split_test_train_val.py
---labelme_2_coco
    python labelme_2_coco.py
```

## For detection
```
---remove the '_connected/_disconnected' suffix from label names.
python generate_detection_data.py
python resize_image_n_annotation.py
python coco_2_kitti.py/coco_2_yolo.py
```

## For classification
