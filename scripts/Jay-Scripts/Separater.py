# import os
# import shutil
# from sklearn.model_selection import train_test_split

# # Define paths
# base_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data"
# images_dir = os.path.join(base_dir, "images")  # Directory containing all images
# labels_dir = os.path.join(base_dir, "labels")  # Directory containing all YOLO annotation files
# output_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/training_dataset"

# # Output directories
# train_images_dir = os.path.join(output_dir, "train/images")
# train_labels_dir = os.path.join(output_dir, "train/labels")
# val_images_dir = os.path.join(output_dir, "val/images")
# val_labels_dir = os.path.join(output_dir, "val/labels")

# # Create output directories if they don't exist
# os.makedirs(train_images_dir, exist_ok=True)
# os.makedirs(train_labels_dir, exist_ok=True)
# os.makedirs(val_images_dir, exist_ok=True)
# os.makedirs(val_labels_dir, exist_ok=True)

# # Get list of images and corresponding labels
# image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
# label_files = sorted([f for f in os.listdir(labels_dir) if f.endswith('.txt')])

# # Ensure each image has a corresponding label
# image_label_pairs = [
#     (os.path.join(images_dir, img), os.path.join(labels_dir, img.replace(img.split('.')[-1], 'txt')))
#     for img in image_files if os.path.exists(os.path.join(labels_dir, img.replace(img.split('.')[-1], 'txt')))
# ]

# # Split into training and validation sets (80-20 split)
# train_pairs, val_pairs = train_test_split(image_label_pairs, test_size=0.2, random_state=42)

# # Move files to the respective directories
# def move_files(pairs, img_dest, lbl_dest):
#     for img_path, lbl_path in pairs:
#         shutil.copy(img_path, img_dest)
#         shutil.copy(lbl_path, lbl_dest)

# # Move training files
# move_files(train_pairs, train_images_dir, train_labels_dir)

# # Move validation files
# move_files(val_pairs, val_images_dir, val_labels_dir)

# print(f"Dataset split completed!")
# print(f"Training images: {len(train_pairs)}, Validation images: {len(val_pairs)}")

# import os
# import shutil

# # Paths
# train_images_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/training_dataset/train/images"
# train_labels_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/training_dataset/train/labels"
# val_images_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/training_dataset/val/images"
# val_labels_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/training_dataset/val/labels"

# # Function to move labels to corresponding image directories
# def move_labels(images_dir, labels_dir):
#     for image_file in os.listdir(images_dir):
#         if image_file.endswith((".jpg", ".png", ".jpeg")):
#             base_name = os.path.splitext(image_file)[0]
#             label_file = f"{base_name}.txt"
#             label_path = os.path.join(labels_dir, label_file)
#             if os.path.exists(label_path):
#                 shutil.move(label_path, images_dir)
#             else:
#                 print(f"Label not found for: {image_file}")

# # Process train and validation sets
# move_labels(train_images_dir, train_labels_dir)
# move_labels(val_images_dir, val_labels_dir)

# print("Labels moved successfully!")

import os
import shutil
from sklearn.model_selection import train_test_split

# Define paths
base_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data"
images_dir = os.path.join(base_dir, "images")  # Directory containing all images
labels_dir = os.path.join(base_dir, "labels")  # Directory containing all YOLO annotation files
output_dir = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/training_dataset"

# Output directories
train_dir = os.path.join(output_dir, "train")
val_dir = os.path.join(output_dir, "val")
test_dir = os.path.join(output_dir, "test")

# Create output directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Get list of images and corresponding labels
image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
label_files = sorted([f for f in os.listdir(labels_dir) if f.endswith('.txt')])

# Ensure each image has a corresponding label
image_label_pairs = [
    (os.path.join(images_dir, img), os.path.join(labels_dir, img.replace(img.split('.')[-1], 'txt')))
    for img in image_files if os.path.exists(os.path.join(labels_dir, img.replace(img.split('.')[-1], 'txt')))
]

# Split into training, validation, and test sets (70-20-10 split)
train_pairs, temp_pairs = train_test_split(image_label_pairs, test_size=0.3, random_state=42)
val_pairs, test_pairs = train_test_split(temp_pairs, test_size=1/3, random_state=42)

# Move files to the respective directories
def move_files(pairs, dest_dir):
    for img_path, lbl_path in pairs:
        shutil.copy(img_path, dest_dir)  # Copy image
        shutil.copy(lbl_path, dest_dir)  # Copy label

# Move training files
move_files(train_pairs, train_dir)

# Move validation files
move_files(val_pairs, val_dir)

# Move test files
move_files(test_pairs, test_dir)

print(f"Dataset split completed!")
print(f"Training images: {len(train_pairs)}, Validation images: {len(val_pairs)}, Test images: {len(test_pairs)}")
