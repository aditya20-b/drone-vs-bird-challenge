import os
import subprocess
import json
from sanityCheck import get_video_frame_count, count_extracted_frames_common_dir, RED, GREEN, YELLOW, RESET

# Paths
video_dir = 'train_videos'
output_dir = 'extracted_frames'
log_file = 'extraction_log.json'

os.makedirs(output_dir, exist_ok=True)

# Initialize log
log_entries = []

# Iterate through videos
for video in os.listdir(video_dir):
    # Fuck you .MP4,
    if video.casefold().endswith(('.mp4', '.avi', '.mpg')):
        video_path = os.path.join(video_dir, video)
        base_name = os.path.splitext(video)[0]
        
        output_path = os.path.join(output_dir, f"{base_name}_%04d.jpg")
        total_frames = get_video_frame_count(video_path)

        # Check existing frames
        extracted_frames = count_extracted_frames_common_dir(output_dir, base_name)

        if extracted_frames == total_frames:
            print(f"{GREEN} ✔️ All frames already extracted for {video}{RESET}")
            continue  # Skip re-extraction

        print(f"{YELLOW} ⚠️ Missing frames detected for {video}. Extracting missing frames...{RESET}")

        # Extract missing frames with ffmpeg
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vsync', '0',
            '-q:v', '2',
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Log entry
        log_entry = {
            'video': video,
            'output_files': total_frames,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
        }

        if result.returncode == 0:
            extracted_frames = count_extracted_frames_common_dir(output_dir, base_name)
            if total_frames == extracted_frames:
                print(f"{GREEN} ✔️ Frames extracted for {video} - Total Frames: {total_frames}, Extracted: {extracted_frames}{RESET}")
            else:
                print(f"{YELLOW} ⚠️ Frame count mismatch for {video} - Total Frames: {total_frames}, Extracted: {extracted_frames}{RESET}")
        else:
            print(f"{RED} ❌ Failed to extract frames for {video}. Check the details below:{RESET}")
            print(result.stderr)

        log_entries.append(log_entry)

# Write log as valid JSON
with open(log_file, 'w') as log:
    json.dump(log_entries, log, indent=4)

print(f"Extraction process completed. Logs saved to {log_file}")
