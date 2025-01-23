import os
import json
import shutil

def setup_video_dir(json_dir, frames_dir, output_dir):
    # Create the output directory and subdirectories
    images_dir = os.path.join(output_dir, 'images')
    labels_dir = os.path.join(output_dir, 'labels')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    # Loop through all JSON files in the directory
    for json_file in os.listdir(json_dir):
        json_path = os.path.join(json_dir, json_file)
        if json_path.endswith('.json'):
            # Load the COCO JSON file
            with open(json_path, 'r') as f:
                coco_data = json.load(f)

            # Create category mapping (COCO class IDs to YOLO class IDs)
            categories = {cat['id']: i for i, cat in enumerate(coco_data['categories'])}
            images = {img['id']: img for img in coco_data['images']}
            annotations = coco_data['annotations']

            # Process each annotation
            for ann in annotations:
                img_info = images[ann['image_id']]
                image_name = img_info['file_name']
                image_width = img_info['width']
                image_height = img_info['height']

                # Copy the corresponding frame to the images directory
                source_frame_path = os.path.join(frames_dir, image_name)
                target_frame_path = os.path.join(images_dir, image_name)
                if not os.path.exists(source_frame_path):
                    print(f"Frame {source_frame_path} not found, skipping.")
                    continue
                shutil.copy2(source_frame_path, target_frame_path)

                # Convert COCO bbox to YOLO format
                x, y, width, height = ann['bbox']
                center_x = (x + width / 2) / image_width
                center_y = (y + height / 2) / image_height
                norm_width = width / image_width
                norm_height = height / image_height
                class_id = categories[ann['category_id']]

                # Write YOLO annotation to file
                yolo_file = os.path.join(labels_dir, image_name.replace('.jpg', '.txt'))
                with open(yolo_file, 'a') as yolo_f:
                    yolo_f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}\n")

    print(f"Directory structure created and data populated in '{output_dir}'.")

# Example usage
json_dir = 'output_json'  # Path to the directory with multiple COCO JSON files
frames_dir = 'extracted_frames'  # Path to the directory with extracted frames
output_dir = 'video_data'  # Output directory to store images and labels
setup_video_dir(json_dir, frames_dir, output_dir)
