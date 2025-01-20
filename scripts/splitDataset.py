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

def split_and_organize_data(mapping_json, yolo_labels_dir, frames_dir_flattened, output_dir, test_size=0.2, val_size=0.1, random_state=42):
    # Load the JSON mapping
    print(f"{CYAN}Loading YOLO labels to frames mapping...{RESET}")
    with open(mapping_json, 'r') as f:
        yolo_labels_to_frames = json.load(f)

    # Create output directories
    dirs = {
        "train": {"labels": os.path.join(output_dir, "labels", "train"), "images": os.path.join(output_dir, "images", "train")},
        "val": {"labels": os.path.join(output_dir, "labels", "val"), "images": os.path.join(output_dir, "images", "val")},
        "test": {"labels": os.path.join(output_dir, "labels", "test"), "images": os.path.join(output_dir, "images", "test")},
    }

    for key in dirs:
        for subdir in dirs[key].values():
            os.makedirs(subdir, exist_ok=True)

    # Prepare data for splitting
    yolo_labels = list(yolo_labels_to_frames.keys())
    frames = [yolo_labels_to_frames[label] for label in yolo_labels]

    # Split data into train+val and test
    print(f"{CYAN}Splitting dataset into train, val, and test...{RESET}")
    train_val_labels, test_labels, train_val_frames, test_frames = train_test_split(
        yolo_labels, frames, test_size=test_size, random_state=random_state
    )

    # Further split train+val into train and val
    val_ratio = val_size / (1 - test_size)  # Adjust validation size relative to the remaining data
    train_labels, val_labels, train_frames, val_frames = train_test_split(
        train_val_labels, train_val_frames, test_size=val_ratio, random_state=random_state
    )

    # Function to move files
    def move_files(labels, frames, labels_dir, frames_dir):
        for label, frame in tqdm(zip(labels, frames), total=len(labels), desc=f"{YELLOW}Moving files{RESET}"):
            # Move label file
            label_src = os.path.join(yolo_labels_dir, label)
            label_dst = os.path.join(labels_dir, label)
            if os.path.exists(label_src):
                shutil.copy(label_src, label_dst)

            # Move frame file
            frame_src = os.path.join(frames_dir_flattened, frame)
            frame_dst = os.path.join(frames_dir, frame)
            if os.path.exists(frame_src):
                shutil.copy(frame_src, frame_dst)

    # Organize data for each split
    print(f"{CYAN}Organizing training data...{RESET}")
    move_files(train_labels, train_frames, dirs["train"]["labels"], dirs["train"]["images"])

    print(f"{CYAN}Organizing validation data...{RESET}")
    move_files(val_labels, val_frames, dirs["val"]["labels"], dirs["val"]["images"])

    print(f"{CYAN}Organizing testing data...{RESET}")
    move_files(test_labels, test_frames, dirs["test"]["labels"], dirs["test"]["images"])

    # Summary
    print(f"{GREEN}Dataset split completed!{RESET}")
    print(f"{GREEN}Train: {len(train_labels)} labels{RESET}, {YELLOW}Validation: {len(val_labels)} labels{RESET}, {RED}Test: {len(test_labels)} labels{RESET}")

# Example usage
mapping_json = "yolo_labels_to_frames.json"
yolo_labels_dir = "coco_to_yolo/flattened"
frames_dir = "extracted_frames"
output_dir = "dataset"

split_and_organize_data(mapping_json, yolo_labels_dir, frames_dir, output_dir)
