import cv2

buffer_pixel = 50
buffer_1 = {
    'jet_bridge': [50, 25, 0, 0],
    'cargo_loader': [-50, 50, 100, 0],
    'belt_loader': [-100, 25, 100, 0],
    'catering_vehicle': [-100, 0, 200, 0],
    'pca': [100, 25, 0, 0],
    'pushback_tug': [0, 100, 25, 0]
}


def crop_classification_1(img, bbox, cat_name):
    if 'connected' or 'disconnected' in cat_name:
        split_name = cat_name.split('_')[:-1]
        cat_name = '_'.join(split_name)

    bbox = [int(abs(x)) for x in bbox]
    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]
    padding_value = buffer_1[cat_name]
    n_x1, n_y1 = x1 - padding_value[0], y1 - padding_value[1]
    n_x2, n_y2 = x2 + padding_value[2], y2 + padding_value[3]
    crop_img = img[n_y1:n_y2, n_x1:n_x2]
    # cv2.imshow("crop_img", crop_img)
    # cv2.waitKey(0)
    return crop_img
