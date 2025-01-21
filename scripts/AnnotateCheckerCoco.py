import os
import json
import cv2
import matplotlib.pyplot as plt

# Paths to COCO annotations and images
annotations_file = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/output_json/2019_08_19_C0001_5319_phantom.json"
images_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/extracted_frames"

# Load COCO annotations
with open(annotations_file, 'r') as f:
    coco_data = json.load(f)

# Map image IDs to file names
image_dict = {img['id']: img for img in coco_data['images']}

# Iterate through annotations and visualize
for annotation in coco_data['annotations']:
    image_id = annotation['image_id']
    bbox = annotation['bbox']  # Format: [x, y, width, height]
    category_id = annotation['category_id']
    category_name = next(cat['name'] for cat in coco_data['categories'] if cat['id'] == category_id)

    # Get corresponding image file
    img_info = image_dict.get(image_id)
    if img_info is None:
        continue
    img_path = os.path.join(images_dir, img_info['file_name'])
    
    # Load the image
    img = cv2.imread(img_path)
    if img is None:
        print(f"Image {img_path} not found!")
        continue

    # Convert BGR to RGB for Matplotlib
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Draw the bounding box
    x, y, w, h = map(int, bbox)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(img, category_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Display the image
    plt.figure(figsize=(10, 6))
    plt.imshow(img)
    plt.title(f"Image ID: {image_id} - Category: {category_name}")
    plt.axis('off')
    plt.show()
