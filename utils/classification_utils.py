import cv2

buffer_pixel = 50
buffer_1 = {
    'jet_bridge': [0.75, 0.1, 0, 0],
    'cargo_loader': [-0.5, 0.25, 0.5, 0],
    'belt_loader': [-0.5, 0.25, 0.75, 0],
    'catering_vehicle': [0, 0, 0.5, -0.5],
    'pca': [0.5, 0.5, 0, 0.5],
    'pushback_tug': [0, 0.5, 0.25, 0]
}


def crop_classification_1(img, bbox, cat_name):
    if 'connected' or 'disconnected' in cat_name:
        split_name = cat_name.split('_')[:-1]
        cat_name = '_'.join(split_name)

    bbox = [int(abs(x)) for x in bbox]
    x1, y1, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
    x2, y2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
    padding_cof = buffer_1[cat_name]
    x1_pad, y1_pad = int(w * padding_cof[0]), int(h * padding_cof[1])
    x2_pad, y2_pad = int(w * padding_cof[2]), int(h * padding_cof[3])
    n_x1, n_y1 = x1 - x1_pad, y1 - y1_pad
    n_x2, n_y2 = x2 + x2_pad, y2 + y2_pad
    crop_img = img[n_y1:n_y2, n_x1:n_x2]
    # cv2.imshow("crop_img", crop_img)
    # cv2.waitKey(0)
    return crop_img
