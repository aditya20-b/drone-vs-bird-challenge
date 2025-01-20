import os
import cv2
import random
import json

# Paths
data_dirs = "extracted_frames"  # Directories containing images and annotations
annotations_dir = "coco_to_yolo/flattened"
output_dir = "verification_output/yolo_labels"  # Directory to save images with drawn annotations
annotations_map_path = "yolo_labels_to_frames.json"  # JSON file mapping annotations to images
os.makedirs(output_dir, exist_ok=True)

# Load annotations mapping
with open(annotations_map_path, "r") as f:
    annotations_map = json.load(f)

# Collect all annotation files from the map
annotation_files = list(annotations_map.keys())

# Sample 10 random annotation files
sampled_annotations = random.sample(annotation_files, min(10, len(annotation_files)))

for annotation_file in sampled_annotations:
    # Get the corresponding image file
    image_file = annotations_map[annotation_file]
    image_path = os.path.join(data_dirs, image_file)

    if image_path is None:
        print(f"Image not found for annotation: {annotation_file}")
        continue

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        continue

    h_img, w_img, _ = image.shape

    # Load YOLO annotations
    annotation_path = os.path.join(annotations_dir, annotation_file)
    if not os.path.exists(annotation_path):
        print(f"Annotation file not found: {annotation_path}")
        continue

    with open(annotation_path, "r") as f:
        lines = f.readlines()

    # Draw bounding boxes
    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center, y_center, width, height = map(float, parts[1:])

        # Convert normalized coordinates to absolute pixel values
        x1 = int((x_center - width / 2) * w_img)
        y1 = int((y_center - height / 2) * h_img)
        x2 = int((x_center + width / 2) * w_img)
        y2 = int((y_center + height / 2) * h_img)

        # Draw bounding box
        color = (0, 255, 0)  # Green color for the bounding box
        thickness = 2
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

        # Add label
        label = f"Class {class_id}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
        text_start = (x1, y1 - 5)
        cv2.rectangle(image, (text_start[0], text_start[1] - text_size[1]), (text_start[0] + text_size[0], text_start[1]), color, -1)
        cv2.putText(image, label, text_start, font, font_scale, (0, 0, 0), font_thickness)

    # Save the image with bounding boxes
    output_path = os.path.join(output_dir, image_file)
    cv2.imwrite(output_path, image)
    print(f"Saved annotated image: {output_path}")
