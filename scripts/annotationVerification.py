import os
import json
import cv2
import random

# Paths
coco_json_path = "combined_annotations.json"  # Path to the COCO JSON file
images_dir = "extracted_frames"  # Path to the images (organized by videoname_frameno.jpg)
output_dir = "verification_output"  # Directory to save images with drawn annotations
os.makedirs(output_dir, exist_ok=True)

# Load COCO JSON
with open(coco_json_path, "r") as f:
    coco_data = json.load(f)

# Create a dictionary mapping image IDs to metadata
image_dict = {img["id"]: img for img in coco_data["images"]}

# Draw bounding boxes on random samples
sampled_annotations = random.sample(coco_data["annotations"], 10)  # Visualize 10 random annotations
for annotation in sampled_annotations:
    img_id = annotation["image_id"]
    image_meta = image_dict[img_id]
    image_path = os.path.join(images_dir, image_meta["file_name"])  # Use file_name for correct mapping

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found: {image_path}")
        continue

    # Get bounding box and category
    x, y, w, h = annotation["bbox"]
    category_id = annotation["category_id"]
    category_name = next(cat["name"] for cat in coco_data["categories"] if cat["id"] == category_id)

    # Draw bounding box
    start_point = (int(x), int(y))
    end_point = (int(x + w), int(y + h))
    color = (0, 255, 0)  # Green color for the bounding box
    thickness = 2
    image = cv2.rectangle(image, start_point, end_point, color, thickness)

    # Add label
    label = f"{category_name} ({category_id})"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
    text_start = (start_point[0], start_point[1] - 5)
    cv2.rectangle(image, (text_start[0], text_start[1] - text_size[1]), (text_start[0] + text_size[0], text_start[1]), color, -1)
    cv2.putText(image, label, text_start, font, font_scale, (0, 0, 0), font_thickness)

    # Save the image with bounding box
    output_path = os.path.join(output_dir, image_meta["file_name"])
    cv2.imwrite(output_path, image)
    print(f"Saved annotated image: {output_path}")
