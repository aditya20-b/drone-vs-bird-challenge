import os
import shutil
from tqdm import tqdm
import json

def convert_coco(json_dir, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of JSON files
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    # Loop through all JSON files in the directory with progress bar
    for json_file in tqdm(json_files, desc="Converting COCO to YOLO"):
        json_path = os.path.join(json_dir, json_file)
        
        # Load the COCO JSON file
        with open(json_path, 'r') as f:
            coco_data = json.load(f)

        # Create category mapping (COCO class IDs to YOLO class IDs)
        categories = {cat['id']: i for i, cat in enumerate(coco_data['categories'])}
        images = {img['id']: img for img in coco_data['images']}
        annotations = coco_data['annotations']

        # Process each annotation
        for ann in tqdm(annotations, desc=f"Processing annotations in {json_file}", leave=False):
            img_info = images[ann['image_id']]
            image_name = img_info['file_name']
            image_width = img_info['width']
            image_height = img_info['height']

            # Convert COCO bbox to YOLO format
            x, y, width, height = ann['bbox']
            center_x = (x + width / 2) / image_width
            center_y = (y + height / 2) / image_height
            norm_width = width / image_width
            norm_height = height / image_height
            class_id = categories[ann['category_id']]

            # Write YOLO annotation to file
            yolo_file = os.path.join(output_dir, image_name.replace('.jpg', '.txt'))
            with open(yolo_file, 'a') as yolo_f:
                yolo_f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}\n")

    print(f"YOLO annotations created in '{output_dir}'.")

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
        convert_coco(json_dir='output_json', output_dir='coco_to_yolo')
    
    map_yolo_labels_to_frames('coco_to_yolo', 'extracted_frames', 'yolo_labels_to_frames.json')