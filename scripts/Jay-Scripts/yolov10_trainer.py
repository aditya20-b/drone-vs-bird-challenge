from ultralytics import YOLO
import cv2

# Load the YOLOv10 model with pre-trained weights
model = YOLO('/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/weights/yolov10s.pt')

# Train the model on your custom dataset
model.train(
    data='/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/scripts/configs/video_data.yaml',  # Dataset YAML file
    epochs=10,               # Number of epochs
    batch=16,                # Batch size
    imgsz=640,               # Image size
    device='cpu'             # Use CPU ('cuda:0' for GPU if available)
)

# Define a function for inference on new data
def infer_and_visualize(image_path, output_path):
    # Read the input image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to read image at {image_path}")
        return

    # Run the model for inference
    results = model(img)

    # Visualize predictions (bounding boxes, labels, scores)
    annotated_frame = results[0].plot()  # Annotated image with predictions

    # Display the result
    cv2.imshow('YOLOv10 Inference', annotated_frame)
    cv2.waitKey(0)  # Wait for user input to close the image window
    cv2.destroyAllWindows()

    # Save the annotated image
    cv2.imwrite(output_path, annotated_frame)
    print(f"Annotated image saved at {output_path}")

# Test inference and visualization
input_image = '/path/to/your/test/image.jpg'  # Replace with your image path
output_image = '/path/to/save/output/image.jpg'  # Replace with your desired output path

infer_and_visualize(input_image, output_image)
