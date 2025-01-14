import os
import subprocess
from sanityCheck import get_video_frame_count, count_extracted_frames, RED, GREEN, YELLOW, RESET
import json
video_dir = 'train_videos'
output_dir = 'extracted_frames'
log_file = 'extraction_log.json'

os.makedirs(output_dir, exist_ok=True)

with open(log_file, 'w') as log:
    log.write('[')
    for video in os.listdir(video_dir):
        if video.endswith(('.mp4', '.avi')):
            video_path = os.path.join(video_dir, video)
            base_name = os.path.splitext(video)[0]
            video_output_dir = os.path.join(output_dir, base_name)

            os.makedirs(video_output_dir, exist_ok=True)
            
            output_path = os.path.join(video_output_dir, f"{base_name}_%04d.jpg")
            
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vsync', '0',
                '-q:v', '2',
                output_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            log_json = {
                'video': video,
                'output_dir': video_output_dir,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }

            log.write(json.dumps(log_json))
            log.write(',\n')
            if result.returncode == 0:
                total_frames = get_video_frame_count(video_path)
                extracted_frames = count_extracted_frames(video)

                if total_frames == extracted_frames:
                    print(f"{GREEN} ✔️ Frames extracted for {video} in {video_output_dir} - Total Frames: {total_frames}, Extracted: {extracted_frames}{RESET}")
                else:
                    print(f"{YELLOW} ⚠️ Frame count mismatch for {video} - Total Frames: {total_frames}, Extracted: {extracted_frames}{RESET}")
            else:
                print(f"{RED} ❌ Failed to extract frames for {video}. Check the details below:{RESET}")
                print(result.stderr)

    log.write(']')