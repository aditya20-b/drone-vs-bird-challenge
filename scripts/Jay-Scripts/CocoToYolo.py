import os
import json
import shutil

def setup_video_dir(json_dir, frames_dir, output_dir):
    # Create the output directory and subdirectories
    images_dir = os.path.join(output_dir, 'images')
    labels_dir = os.path.join(output_dir, 'labels')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    # Loop through all JSON files in the directory
    for json_file in os.listdir(json_dir):
        json_path = os.path.join(json_dir, json_file)
        if json_path.endswith('.json'):
            # Load the COCO JSON file
            with open(json_path, 'r') as f:
                coco_data = json.load(f)

            # Create category mapping (COCO class IDs to YOLO class IDs)
            categories = {cat['id']: i for i, cat in enumerate(coco_data['categories'])}
            images = {img['id']: img for img in coco_data['images']}
            annotations = coco_data['annotations']

            # Process each annotation
            for ann in annotations:
                img_info = images[ann['image_id']]
                image_name = img_info['file_name']
                image_width = img_info['width']
                image_height = img_info['height']

                # Copy the corresponding frame to the images directory
                source_frame_path = os.path.join(frames_dir, image_name)
                target_frame_path = os.path.join(images_dir, image_name)
                if not os.path.exists(source_frame_path):
                    print(f"Frame {source_frame_path} not found, skipping.")
                    continue
                shutil.copy2(source_frame_path, target_frame_path)

                # Convert COCO bbox to YOLO format
                x, y, width, height = ann['bbox']
                center_x = (x + width / 2) / image_width
                center_y = (y + height / 2) / image_height
                norm_width = width / image_width
                norm_height = height / image_height
                class_id = categories[ann['category_id']]

                # Write YOLO annotation to file
                yolo_file = os.path.join(labels_dir, image_name.replace('.jpg', '.txt'))
                with open(yolo_file, 'a') as yolo_f:
                    yolo_f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}\n")

    print(f"Directory structure created and data populated in '{output_dir}'.")

# Example usage
json_dir = 'output_json'  # Path to the directory with multiple COCO JSON files
frames_dir = 'extracted_frames'  # Path to the directory with extracted frames
output_dir = 'video_data'  # Output directory to store images and labels
setup_video_dir(json_dir, frames_dir, output_dir)


# import os
# import cv2
# import json

# def coco_to_yolo(coco_bbox, img_w, img_h):
#     x, y, w, h = coco_bbox
#     center_x = (x + w / 2) / img_w
#     center_y = (y + h / 2) / img_h
#     norm_w = w / img_w
#     norm_h = h / img_h
#     return center_x, center_y, norm_w, norm_h

# def process_images(frames_dir, coco_annotations_file, output_dir):
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     yolo_labels_dir = os.path.join(output_dir, "labels")
#     annotated_images_dir = os.path.join(output_dir, "annotated")
#     os.makedirs(yolo_labels_dir, exist_ok=True)
#     os.makedirs(annotated_images_dir, exist_ok=True)
    
#     with open(coco_annotations_file, 'r') as f:
#         coco_data = json.load(f)
    
#     image_dict = {img['file_name']: img for img in coco_data['images']}
#     annotations_dict = {ann['image_id']: [] for ann in coco_data['annotations']}
#     for ann in coco_data['annotations']:
#         annotations_dict[ann['image_id']].append(ann)
    
#     for img_name, img_info in image_dict.items():
#         image_path = os.path.join(frames_dir, img_name)
#         if not os.path.exists(image_path):
#             continue
        
#         image = cv2.imread(image_path)
#         img_h, img_w = image.shape[:2]
#         image_id = img_info['id']
        
#         yolo_annotations = []
        
#         for annotation in annotations_dict.get(image_id, []):
#             coco_bbox = annotation['bbox']
#             class_id = 0
#             center_x, center_y, norm_w, norm_h = coco_to_yolo(coco_bbox, img_w, img_h)
#             yolo_annotations.append(f"{class_id} {center_x:.6f} {center_y:.6f} {norm_w:.6f} {norm_h:.6f}")
            
#             x1 = int((center_x - norm_w / 2) * img_w)
#             y1 = int((center_y - norm_h / 2) * img_h)
#             x2 = int((center_x + norm_w / 2) * img_w)
#             y2 = int((center_y + norm_h / 2) * img_h)
            
#             cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(image, f"Class {int(class_id)}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
#         yolo_label_path = os.path.join(yolo_labels_dir, f"{os.path.splitext(img_name)[0]}.txt")
#         with open(yolo_label_path, 'w') as label_file:
#             label_file.write('\n'.join(yolo_annotations))
        
#         annotated_image_path = os.path.join(annotated_images_dir, img_name)
#         cv2.imwrite(annotated_image_path, image)
        
#         print(f"Processed: {img_name}, Annotations saved: {yolo_label_path}, Image saved: {annotated_image_path}")

# frames_directory = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/images"
# coco_annotations_file = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/output_json/2019_08_19_C0001_5319_phantom.json'
# output_directory = "/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/checker_dummy"
# process_images(frames_directory, coco_annotations_file, output_directory)
