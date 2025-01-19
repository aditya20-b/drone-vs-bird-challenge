import json
import os

# Input and output paths
input_dir = "output_json"  # Directory with video-specific COCO JSON files
output_file = "combined_annotations.json"

combined_data = {"images": [], "annotations": [], "categories": []}
image_id_offset = 1
annotation_id_offset = 1

for json_file in os.listdir(input_dir):
    if json_file.endswith(".json"):
        with open(os.path.join(input_dir, json_file), "r") as f:
            data = json.load(f)

        # Adjust image and annotation IDs to avoid duplicates
        for img in data["images"]:
            img["id"] += image_id_offset
            combined_data["images"].append(img)

        for ann in data["annotations"]:
            ann["id"] += annotation_id_offset
            ann["image_id"] += image_id_offset
            combined_data["annotations"].append(ann)

        image_id_offset = max(img["id"] for img in combined_data["images"]) + 1
        annotation_id_offset = max(ann["id"] for ann in combined_data["annotations"]) + 1

        # Add categories (ensure no duplicates)
        for cat in data["categories"]:
            if cat not in combined_data["categories"]:
                combined_data["categories"].append(cat)

# Write combined JSON
with open(output_file, "w") as f:
    json.dump(combined_data, f, indent=4)

print(f"Combined annotations saved to {output_file}")
