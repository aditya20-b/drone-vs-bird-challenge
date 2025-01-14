import os
import subprocess

video_dir = 'train_videos'
frames_dir = 'extracted_frames'

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Get frame count for each video using ffprobe
def get_video_frame_count(video_path):
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-count_frames', '-show_entries', 'stream=nb_read_frames',
        '-of', 'default=nokey=1:noprint_wrappers=1', video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0

# Count extracted frames for each video directory
def count_extracted_frames(video_name: str) -> int:
    video_frames_dir = os.path.join(frames_dir, video_name.split('.')[0])
    if os.path.exists(video_frames_dir):
        return len([f for f in os.listdir(video_frames_dir) if f.endswith('.jpg')])
    return 0

# Perform sanity check
def sanity_check():
    discrepancies = []
    frame_count = 0
    for video in os.listdir(video_dir):
        if video.endswith(('.mp4', '.avi')):
            video_path = os.path.join(video_dir, video)
            base_name = os.path.splitext(video)[0]  # Base name without extension
            
            total_frames = get_video_frame_count(video_path)
            extracted_frames = count_extracted_frames(base_name)
            
            if total_frames != extracted_frames:
                discrepancies.append((video, total_frames, extracted_frames))
                print(f"{YELLOW}{video}: Total Frames = {total_frames}, Extracted = {extracted_frames}{RESET}")
                frame_count += extracted_frames
            else:
                print(f"{GREEN}{video}: Total Frames = {total_frames}, Extracted = {extracted_frames}{RESET}")

    # Print discrepancies
    if discrepancies:
        print(f"\n{RED}Discrepancies Found:{RESET}")
        for video, total, extracted in discrepancies:
            print(f"{RED}{video}: Expected {total}, but got {extracted}{RESET}")
    else:
        print(f"\n{GREEN}All videos have correct frame extraction!{RESET}")

    print(f"\nTotal Frames Extracted: {frame_count}")

if __name__ == "__main__":
    sanity_check()
