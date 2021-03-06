import cv2
import os
from tqdm import tqdm
import yaml


def video_to_frames(video, path_output_dir, count):
    vid_cap = cv2.VideoCapture(video)

    while vid_cap.isOpened():
        success, image = vid_cap.read()
        if success:
            count += 1
            if count % multiple_factor == 0:
                value = count // multiple_factor
                split_segment = video_segment.split('_')
                airport_w_stand = split_segment[0] + '_' + split_segment[1]
                segment_num = video_segment.split('_')[-1]
                value = airport_w_stand + '_' + 'v' + segment_num + '_' + str(value).zfill(6)
                cv2.imwrite(os.path.join(path_output_dir, value + '.jpg'), image)
                # print(value)
            # Display the resulting frame
            # cv2.imshow('frame', image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        else:
            break
    cv2.destroyAllWindows()
    vid_cap.release()
    return count


if __name__ == '__main__':
    with open('params.yaml') as f:
        my_dict = yaml.safe_load(f)
    os.chdir(r"..\\")

    video_path = os.getcwd() + '/' + my_dict['video']['video_path']
    video_segment = my_dict['video']['video_segment']
    segment_list = os.listdir(video_path + '/' + video_segment)
    segment_list = sorted(segment_list, reverse=False)
    segment_list = [segment for segment in segment_list if segment.endswith('.mp4')]
    if not os.path.exists(os.getcwd() + '/' + my_dict['video']['save_img_dir'] + '/' + video_segment):
        os.mkdir(os.getcwd() + '/' + my_dict['video']['save_img_dir'] + '/' + video_segment)
    combine_flag = True

    if combine_flag:
        output_dir = os.getcwd() + '/' + my_dict['video']['save_img_dir'] + '/' + video_segment
        file_list_output_dir = os.listdir(output_dir)
        file_list_output_dir = sorted(file_list_output_dir, reverse=True)
        frame_count = 0
        multiple_factor = my_dict['video']['multiple_factor']
        if len(file_list_output_dir) > 0:
            last_file_name = file_list_output_dir[0].split('.')
            frame_count = int(last_file_name[0]) * multiple_factor

        for file in tqdm(segment_list):
            video_file = os.path.join(video_path + '/' + video_segment, file)
            last_frame_count = video_to_frames(video_file, output_dir, frame_count)
            frame_count = last_frame_count

    else:
        file_list_output_dir = os.listdir(video_segment)
        # print(file_list_output_dir)
        file_list_output_dir = sorted(file_list_output_dir, reverse=True)
        video_file = os.path.join(video_path + video_segment, 'segment_piece_last.mp4')
        video_to_frames(video_file, video_segment)



