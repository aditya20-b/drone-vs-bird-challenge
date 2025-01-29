import os
import cv2
import json
import matplotlib.pyplot as plt

def visualize_frame_annotation(image_path, label_path, coco_annotations_file):
    """
    Visualizes both YOLO and COCO annotations by overlaying bounding boxes on a single image.
    
    Args:
        image_path (str): Path to the image file (frame).
        label_path (str): Path to the YOLO annotation file.
        coco_annotations_file (str): Path to the COCO annotations file.
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image: {image_path}")
        return

    # Read YOLO annotations and draw bounding boxes
    with open(label_path, 'r') as f:
        for line in f:
            class_id, center_x, center_y, width, height = map(float, line.strip().split())
            img_h, img_w = image.shape[:2]

            # Convert YOLO format to pixel-based COCO coordinates
            x1 = int((center_x - width / 2) * img_w)
            y1 = int((center_y - height / 2) * img_h)
            x2 = int((center_x + width / 2) * img_w)
            y2 = int((center_y + height / 2) * img_h)

            # Draw the YOLO bounding box (green color)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"YOLO Class {int(class_id)}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Load COCO annotations
    with open(coco_annotations_file, 'r') as f:
        coco_data = json.load(f)

    # Map image file names to their corresponding image IDs
    image_name = os.path.basename(image_path)
    image_dict = {img['file_name']: img for img in coco_data['images']}
    img_info = image_dict.get(image_name)

    if img_info is None:
        print(f"No annotations found for image: {image_name}")
        return

    image_id = img_info['id']
    annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_id]

    if not annotations:
        print(f"No annotations found for image: {image_name}")
        return

    # Iterate through annotations for the image and draw bounding boxes
    for annotation in annotations:
        bbox = annotation['bbox']  # Format: [x, y, width, height]
        category_id = annotation['category_id']
        category_name = next(cat['name'] for cat in coco_data['categories'] if cat['id'] == category_id)

        # Draw the bounding box (red color)
        x, y, w, h = map(int, bbox)
        print(f"COCO Format: x: {x}, y: {y}, width: {w}, height: {h}")
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, category_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Display the image with both YOLO and COCO annotations
    cv2.imshow('YOLO and COCO Annotations', image)
    cv2.waitKey(0)  # Wait for any key press to close the window
    cv2.destroyAllWindows()

# Example usage
image_path = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/images/2019_10_16_C0003_1700_matrice_0934.jpg'  # Path to the image (frame)
label_path = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/labels/2019_10_16_C0003_1700_matrice_0934.txt'  # Path to the corresponding YOLO annotation file
coco_annotations_file = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/output_json/2019_10_16_C0003_1700_matrice.json'  # Path to the COCO annotations file

visualize_frame_annotation(image_path, label_path, coco_annotations_file)