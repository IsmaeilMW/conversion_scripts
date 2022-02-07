## Folder structure to follow
```
data
    annotation
        video_1
            labels_files(*.json)
        video_2
        -------
        -------
    images
        video_1
            image_files(*.jpg)
        video_2
        -------
        -------
    live_feed
        feed from server stored here.
    conversion_scripts
        python transfer_files.py
        python split_test_train_val.py
        ------------------
        ------------------
        
    model_data(Data used for model training.)
        datasets
            1
                images(selected images from different video files)
                    video_1
                    video_2
                    video_3
                    --------
                    -------
                annotation(selected labels from different annotation)
                    video_1
                    video_2
                    video_3
                    -------
                    -------
                merge_files
                    ## Files from different directory combine into 1
                    ## merge_files.py
                    images(*.jpg)
                    annotation(.json)
                ## using data from merge file directory create test/train/val files
                test
                    '.jpg'
                    '.json'
                train
                    '.jpg'
                    '.json'
                val
                    '.jpg'
                    '.json'
                
```

##Order to follow
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
python coco_2_yolo.py
python coco_2_kitti.py
```

## For classification
```
python generate_classification_data.py
```
