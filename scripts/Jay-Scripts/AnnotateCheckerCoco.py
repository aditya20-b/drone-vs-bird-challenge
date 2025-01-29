import os
import json
import cv2
import matplotlib.pyplot as plt

def visualize_coco_annotation(image_path, annotations_file):
    """
    Visualizes COCO annotations by overlaying bounding boxes on an image.
    
    Args:
        image_path (str): Path to the image file.
        annotations_file (str): Path to the COCO annotations file.
    """
    # Load COCO annotations
    with open(annotations_file, 'r') as f:
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

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Image {image_path} not found!")
        return

    # Convert BGR to RGB for Matplotlib
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Iterate through annotations for the image and draw bounding boxes
    for annotation in annotations:
        bbox = annotation['bbox']  # Format: [x, y, width, height]
        category_id = annotation['category_id']
        category_name = next(cat['name'] for cat in coco_data['categories'] if cat['id'] == category_id)

        # Draw the bounding box
        x, y, w, h = map(int, bbox)
        print(f"COCO Format: x: {x}, y: {y}, width: {w}, height: {h}")
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, category_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Display the image
    plt.figure(figsize=(10, 6))
    plt.imshow(img)
    plt.title(f"Image: {image_name}")
    plt.axis('off')
    plt.show()

# Example usage
image_path = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/extracted_frames/two_uavs_plus_airplane_1300.jpg"  # Path to the individual image file (frame)
annotations_file = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/output_json/two_uavs_plus_airplane.json"  # Path to the COCO annotations file

visualize_coco_annotation(image_path, annotations_file)