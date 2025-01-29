import os
import cv2

def visualize_frame_annotation(image_path, label_path):
    """
    Visualizes both YOLO and COCO annotations by overlaying bounding boxes on a single image.
    
    Args:
        image_path (str): Path to the image file (frame).
        label_path (str): Path to the YOLO annotation file.
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

            # Print YOLO format
            print(f"YOLO Format: Class {int(class_id)}, Center: ({center_x:.4f}, {center_y:.4f}), Width: {width:.4f}, Height: {height:.4f}")
            
            # Print COCO format
            print(f"COCO Format: x: {int(x1)}, y: {int(y1)}, width: {int(x2 - x1)}, height: {int(y2 - y1)}")

            # Draw the YOLO bounding box on the image (green color)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"YOLO Class {int(class_id)}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Visualizing COCO format annotation on the same image (red color)
            coco_x1 = x1  # Same as YOLO x1
            coco_y1 = y1  # Same as YOLO y1
            coco_x2 = x2  # Same as YOLO x2
            coco_y2 = y2  # Same as YOLO y2

            # Draw the COCO bounding box (red color)
            cv2.rectangle(image, (coco_x1, coco_y1), (coco_x2, coco_y2), (0, 0, 255), 2)
            cv2.putText(image, f"COCO Class {int(class_id)}", (coco_x1, coco_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the image with both annotations
    cv2.imshow('YOLO and COCO Annotations', image)
    cv2.waitKey(0)  # Wait for any key press to close the window
    cv2.destroyAllWindows()

# Example usage
image_path = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/extracted_frames/two_uavs_plus_airplane_1300.jpg'  # Path to the image (frame)
label_path = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/labels/two_uavs_plus_airplane_1300.txt'  # Path to the corresponding YOLO annotation file

visualize_frame_annotation(image_path, label_path)
