from ultralytics import YOLO

# Load the YOLOv10 model with pre-trained weights
model = YOLO('/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/weights/yolov10s.pt')

# Train the model on your custom dataset
model.train(
    data='/Users/jayashre/Developer/VSC/drone-vs-bird-challenge/scripts/configs/video_data.yaml',     # Path to your dataset YAML file
    epochs=10,                  # Number of epochs
    batch=16,                   # Batch size
    imgsz=640,                  # Image size
    device='cpu'                    # Use GPU (set to 0 for first GPU)
)
