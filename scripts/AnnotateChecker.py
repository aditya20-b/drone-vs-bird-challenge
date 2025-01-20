import os
import cv2

def visualize_annotations(images_dir, labels_dir, output_dir=None):
    """
    Visualizes YOLO annotations by overlaying bounding boxes on images.
    
    Args:
        images_dir (str): Directory containing the images.
        labels_dir (str): Directory containing YOLO annotation files.
        output_dir (str): Directory to save annotated images (optional). If None, images will be displayed.
    """
    os.makedirs(output_dir, exist_ok=True) if output_dir else None

    for image_file in os.listdir(images_dir):
        if not image_file.endswith('.jpg'):
            continue
        
        # Load image
        image_path = os.path.join(images_dir, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image: {image_path}")
            continue

        # Corresponding label file
        label_file = image_file.replace('.jpg', '.txt')
        label_path = os.path.join(labels_dir, label_file)
        if not os.path.exists(label_path):
            print(f"No annotation file for image: {image_file}")
            continue

        # Read YOLO annotations and draw bounding boxes
        with open(label_path, 'r') as f:
            for line in f:
                class_id, center_x, center_y, width, height = map(float, line.strip().split())
                img_h, img_w = image.shape[:2]
                x1 = int((center_x - width / 2) * img_w)
                y1 = int((center_y - height / 2) * img_h)
                x2 = int((center_x + width / 2) * img_w)
                y2 = int((center_y + height / 2) * img_h)

                # Draw bounding box and label
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f"Class {int(class_id)}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save or display the image
        if output_dir:
            output_path = os.path.join(output_dir, image_file)
            cv2.imwrite(output_path, image)
        else:
            cv2.imshow('Annotation Visualization', image)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break

    if not output_dir:
        cv2.destroyAllWindows()

# Example usage
images_dir = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/images'  # Directory containing images
labels_dir = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/video_data/labels'  # Directory containing YOLO annotations
output_dir = '/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/annotated_images'  # Directory to save annotated images (optional)

visualize_annotations(images_dir, labels_dir, output_dir)
