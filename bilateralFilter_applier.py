''''Apply the bilateral filter to entire video without loosing any frames'''

import cv2
import os

def split_video(video_path, output_dir):
    # Create directory to save frames
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Capture video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    return frame_count

def process_frame(frame):
    # Apply bilateral filter
    return cv2.bilateralFilter(frame, d=9, sigmaColor=75, sigmaSpace=75)

def merge_frames_to_video(output_dir, output_video_path, frame_rate):
    # Get frame size and initialize video writer
    first_frame = cv2.imread(os.path.join(output_dir, 'frame_0000.png'))
    height, width, layers = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])
    for frame_file in frame_files:
        frame_path = os.path.join(output_dir, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()

def main(video_path, output_dir, output_video_path):
    # Step 1: Split the video into frames
    frame_count = split_video(video_path, output_dir)

    # Step 2: Process each frame with bilateral filter
    for i in range(frame_count):
        frame_path = os.path.join(output_dir, f'frame_{i:04d}.png')
        frame = cv2.imread(frame_path)
        processed_frame = process_frame(frame)
        cv2.imwrite(frame_path, processed_frame)

    # Step 3: Merge processed frames back into a video
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    merge_frames_to_video(output_dir, output_video_path, frame_rate)

if __name__ == "__main__":
    video_path = 'input_video.mp4'  # Path to the input video
    output_dir = 'output_frames'    # Directory to save frames
    output_video_path = 'output_video.mp4'  # Path to save the output video

    main(video_path, output_dir, output_video_path)
