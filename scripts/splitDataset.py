import os
import json
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# ANSI codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

# Paths
frames_dir = "extracted_frames"
annotations_path = "combined_annotations.json"
output_frames_dir = "dataset/images"
output_annotations_dir = "dataset/annotations"

os.makedirs(f"{output_frames_dir}/train", exist_ok=True)
os.makedirs(f"{output_frames_dir}/val", exist_ok=True)
os.makedirs(f"{output_frames_dir}/test", exist_ok=True)
os.makedirs(output_annotations_dir, exist_ok=True)

# Load annotations
print(f"{CYAN}Loading annotations...{RESET}")
with open(annotations_path, "r") as f:
    annotations = json.load(f)

# Extract images and annotations
images = annotations["images"]
annotations_list = annotations["annotations"]
categories = annotations["categories"]

# Split images into train, val, and test
print(f"{CYAN}Splitting dataset into train, val, and test...{RESET}")
train_images, temp_images = train_test_split(images, test_size=0.3, random_state=42)
val_images, test_images = train_test_split(temp_images, test_size=0.5, random_state=42)

# Map image IDs to their corresponding annotations
def filter_annotations(image_ids):
    return [ann for ann in annotations_list if ann["image_id"] in image_ids]

# Prepare annotations for each split
print(f"{CYAN}Filtering annotations for each split...{RESET}")
train_annotations = filter_annotations({img["id"] for img in train_images})
val_annotations = filter_annotations({img["id"] for img in val_images})
test_annotations = filter_annotations({img["id"] for img in test_images})

# Save new COCO JSON files
def save_coco_json(images, annotations, output_path):
    coco_format = {
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }
    with open(output_path, "w") as f:
        json.dump(coco_format, f, indent=4)

print(f"{CYAN}Saving new COCO JSON files...{RESET}")
save_coco_json(train_images, train_annotations, os.path.join(output_annotations_dir, "train.json"))
save_coco_json(val_images, val_annotations, os.path.join(output_annotations_dir, "val.json"))
save_coco_json(test_images, test_annotations, os.path.join(output_annotations_dir, "test.json"))

# Move frames to respective directories
print(f"{CYAN}Moving frames to respective directories...{RESET}")
for split_images, split_dir in zip([train_images, val_images, test_images], ["train", "val", "test"]):
    for img in tqdm(split_images, desc=f"{YELLOW}Processing {split_dir} images{RESET}"):
        src = os.path.join(frames_dir, img["file_name"])
        dst = os.path.join(output_frames_dir, split_dir, img["file_name"])
        if os.path.exists(src):
            shutil.copy(src, dst)

print(f"{GREEN}Dataset split completed!{RESET}")
print(f"{GREEN}Train: {len(train_images)} images{RESET}, {YELLOW}Val: {len(val_images)} images{RESET}, {RED}Test: {len(test_images)} images.{RESET}")
