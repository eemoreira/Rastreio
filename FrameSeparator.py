import cv2 as cv
import os

video_path = "videos/MonsterNoBackground.mp4"
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

cap = cv.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_count = 0

while True:
 ret, frame = cap.read()
 if not ret:
     break

 frame_name = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
 cv.imwrite(frame_name, frame)

 frame_count += 1

cap.release()