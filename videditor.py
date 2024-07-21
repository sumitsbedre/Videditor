import os
import moviepy.editor as mp
import cv2

def cut_video(input_path, output_path, start_time, end_time):
    video = mp.VideoFileClip(input_path).subclip(start_time, end_time)
    video.write_videofile(output_path, codec='libx264', fps=24, preset='medium')

def cut_video_into_sections(input_path, section_length):
    video = mp.VideoFileClip(input_path)
    video_duration = video.duration
    start_time = 0
    part = 1

    while start_time < video_duration:
        end_time = start_time + section_length
        if end_time > video_duration:
            end_time = video_duration
        output_path = f"{input_path.split('.')[0]}_part{part}.mp4"
        cut_video(input_path, output_path, start_time, end_time)
        print(f"Saved part {part} from {start_time} to {end_time} seconds as {output_path}")
        start_time = end_time
        part += 1

def extract_frames(input_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    video = cv2.VideoCapture(input_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    count = 0
    success, image = video.read()
    while success:
        frame_path = os.path.join(output_folder, f"{count:04d}.png")
        cv2.imwrite(frame_path, image)
        success, image = video.read()
        count += 1
    video.release()
    print(f"Extracted {count} frames at {fps} FPS to folder: {output_folder}")

def check_consecutiveness(frame_files):
    frame_numbers = [int(f.split('.')[0]) for f in frame_files]
    frame_numbers.sort()
    missing_frames = []
    for i in range(len(frame_numbers) - 1):
        if frame_numbers[i + 1] != frame_numbers[i] + 1:
            for j in range(frame_numbers[i] + 1, frame_numbers[i + 1]):
                missing_frames.append(j)
    return missing_frames

def merge_frames_to_video(input_folder, output_path, fps):
    frame_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')], key=lambda x: int(x.split('.')[0]))
    if not frame_files:
        print("No frames found in the folder.")
        return

    missing_frames = check_consecutiveness(frame_files)
    if missing_frames:
        print(f"Missing frames detected: {missing_frames}")
        response = input("Do you want to continue without the missing frames? (yes/no): ")
        if response.lower() != 'yes':
            for missing_frame in missing_frames:
                missing_frame_str = f"{missing_frame:04d}.png"
                print(f"Searching for missing frame: {missing_frame_str}")
                frame_path = os.path.join(input_folder, missing_frame_str)
                if not os.path.exists(frame_path):
                    print(f"Missing frame {missing_frame_str} not found.")
                    continue_response = input("Do you want to continue without the missing frames? (yes/no): ")
                    if continue_response.lower() != 'yes':
                        print("Exiting without creating video.")
                        return

    first_frame = cv2.imread(os.path.join(input_folder, frame_files[0]))
    height, width, layers = first_frame.shape

    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for frame_file in frame_files:
        frame_number = int(frame_file.split('.')[0])
        if frame_number in missing_frames:
            continue
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        video.write(frame)

    video.release()
    print(f"Video created and saved to {output_path}")

def main():
    while True:
        print("\nVideo Editing Menu")
        print("1. Cut video into smaller parts")
        print("2. Cut video into sections of desired seconds")
        print("3. Extract each frame of the video")
        print("4. Merge frames into a video")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            input_path = input("Enter the path to the input video file: ")
            output_path = input("Enter the path to save the output video file: ")
            start_time = float(input("Enter the start time in seconds: "))
            end_time = float(input("Enter the end time in seconds: "))

            cut_video(input_path, output_path, start_time, end_time)
            print(f"Video has been cut and saved to {output_path}")

        elif choice == '2':
            input_path = input("Enter the path to the input video file: ")
            section_length = float(input("Enter the section length in seconds: "))
            
            cut_video_into_sections(input_path, section_length)

        elif choice == '3':
            input_path = input("Enter the path to the input video file: ")
            output_folder = input("Enter the folder to save the extracted frames: ")

            extract_frames(input_path, output_folder)

        elif choice == '4':
            input_folder = input("Enter the folder containing the frames: ")
            output_path = input("Enter the path to save the output video file: ")
            fps = int(input("Enter the desired frames per second (FPS): "))

            merge_frames_to_video(input_folder, output_path, fps)

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
