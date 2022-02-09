import cv2
import os
from tqdm import tqdm

os.chdir(r"..\\")

video_path = 'images/'
video_segment = 'video_1'
file_list = os.listdir(os.getcwd() + '/' + video_path + video_segment)


def images_2_videos(image_path, path_output_dir):
    size = 1280, 720
    video_file = cv2.VideoWriter(path_output_dir + '/' + 'out_' + video_segment + '.avi',
                                 cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
    for file in tqdm(image_path):
        img = cv2.imread(os.getcwd() + '/' + video_path + video_segment + '/' + file)
        resize_img = cv2.resize(img, size)
        video_file.write(resize_img)
    video_file.release()


if __name__ == '__main__':
    if not os.path.exists(os.getcwd() + '/test_video/' + video_segment):
        os.mkdir(os.getcwd() + '/test_video/' + video_segment)

    images_2_videos(file_list, os.getcwd() + '/test_video/')



