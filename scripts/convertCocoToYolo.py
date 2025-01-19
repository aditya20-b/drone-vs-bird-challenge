from ultralytics.data.converter import convert_coco
import os
import shutil
from tqdm import tqdm
import json

def flatten_dir(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for root, _, files in os.walk(source_dir):
        for file in tqdm(files, desc=f"Processing files in {root}", leave=False):
            if file.endswith('.txt'):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                shutil.copy2(source_file, target_file)
    print(f"Flattened {source_dir} to {target_dir}")

def map_yolo_labels_to_frames(yolo_labels_dir, frames_dir, output_json='yolo_labels_to_frames.json'):
    yolo_labels = os.listdir(yolo_labels_dir)
    frames = os.listdir(frames_dir)
    
    yolo_labels.sort()
    frames.sort()

    # This mapping saves us O(n^2) time complexity
    # using data structures in real life do be crazy
    frame_map = {frame.split('.')[0]: frame for frame in frames}
    
    yolo_labels_to_frames = {}
    for yolo_label in yolo_labels:
        yolo_label_name = yolo_label.split('.')[0]
        # frame_map would almost always be a superset of yolo_labels but just in case
        if yolo_label_name in frame_map:
            yolo_labels_to_frames[yolo_label] = frame_map[yolo_label_name]
    
    
    with open(output_json, 'w') as f:
        json.dump(yolo_labels_to_frames, f, indent=4)

    print(f"Found {len(yolo_labels)} yolo labels and {len(frames)} frames")
    print(f"Matched {len(yolo_labels_to_frames)} yolo labels to frames")
    print(f"Found {len(yolo_labels) - len(yolo_labels_to_frames)} yolo labels without matching frames")
    print(f"Saved yolo labels to frames mapping to {output_json}")
    return yolo_labels_to_frames


if __name__ == '__main__':
    if not os.path.exists('coco_to_yolo'):
        convert_coco(labels_dir='output_json', save_dir='coco_to_yolo')
    
    flatten_dir('coco_to_yolo/labels', 'coco_to_yolo/flattened')
    map_yolo_labels_to_frames('coco_to_yolo/flattened', 'extracted_frames', 'yolo_labels_to_frames.json')