import cv2 as cv
import os

# Diretórios de frames e saída de vídeos
directories = [
    "VideoFrameMatchingNoBackground/TM_CCOEFF_NORMED",
    "VideoFrameMatchingNoBackground/TM_CCORR_NORMED",
    "VideoFrameMatchingWithBackground/TM_CCOEFF_NORMED",
    "VideoFrameMatchingWithBackground/TM_CCORR_NORMED"
]
output_videos = [
    "output/TM_CCOEFF_NORMED_NoBackground.mp4",
    "output/TM_CCORR_NORMED_NoBackground.mp4",
    "output/TM_CCOEFF_NORMED_WithBackground.mp4",
    "output/TM_CCORR_NORMED_WithBackground.mp4"
]

frame_rate = 30  # Taxa de quadros dos vídeos

for frames_dir, output_video_path in zip(directories, output_videos):
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    
    if not frame_files:
        print(f"Error: No frames found in the directory {frames_dir}.")
        continue

    first_frame = cv.imread(os.path.join(frames_dir, frame_files[0]))
    height, width, _ = first_frame.shape

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video_writer = cv.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    for frame_file in frame_files:
        frame_path = os.path.join(frames_dir, frame_file)
        frame = cv.imread(frame_path)
        video_writer.write(frame)

    video_writer.release()
    print(f"Video saved at {output_video_path}")

