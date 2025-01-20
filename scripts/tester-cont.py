import json
import os

def coco_to_yolo(coco_json_path, output_dir):
    # Load the COCO JSON file
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)

    categories = {cat['id']: i for i, cat in enumerate(coco_data['categories'])}
    images = {img['id']: img for img in coco_data['images']}
    annotations = coco_data['annotations']

    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each annotation
    for ann in annotations:
        image_info = images[ann['image_id']]
        image_width = image_info['width']
        image_height = image_info['height']
        file_name = os.path.splitext(image_info['file_name'])[0] + ".txt"

        # Convert COCO bbox to YOLO format
        x, y, width, height = ann['bbox']
        center_x = (x + width / 2) / image_width
        center_y = (y + height / 2) / image_height
        norm_width = width / image_width
        norm_height = height / image_height
        class_id = categories[ann['category_id']]

        # Write to YOLO file
        yolo_annotation = f"{class_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}\n"
        output_file_path = os.path.join(output_dir, file_name)

        with open(output_file_path, 'a') as yolo_file:
            yolo_file.write(yolo_annotation)

    print(f"COCO annotations successfully converted to YOLO format in '{output_dir}'.")

# Example usage
coco_json_path = '00_01_52_to_00_01_58.json'  # Path to your uploaded file
output_dir = 'yolo_labels'  # Directory to save YOLO annotations
coco_to_yolo(coco_json_path, output_dir)
