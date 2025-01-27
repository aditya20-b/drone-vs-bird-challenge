# %%
import ultralytics
from ultralytics import YOLO

# %%
ultralytics.checks()

# %%
model = YOLO('yolo11m.pt')  # 'n' denotes the nano version

# %%
model.device

# %%
model.train(
    data='dataset.yaml',  # Path to the dataset configuration file
    epochs=50,            # Number of training epochs
    imgsz=1024,            # Image size for training
    batch=16,             # Batch size (adjust based on your hardware capabilities)
    name='drone_vs_bird_finetune',  # Name of the training run
    pretrained=True,      # Use pre-trained weights
    device=0,         # GPU device index (set to 'cpu' on mac, GPU acceration is only for CUDA)
    workers=12,            # Number of workers
    amp=True,              # Enable Automatic Mixed Precision (for faster training)     
)


# %% [markdown]
# Ultralytics 8.3.63 🚀 Python-3.10.16 torch-2.5.1 CPU (Apple M3)
# [34m[1mengine/trainer: [0mtask=detect, mode=train, model=yolo11n.pt, data=dataset.yaml, epochs=50, time=None, patience=100, batch=16, imgsz=640, save=True, save_period=-1, cache=False, device=cpu, workers=8, project=None, name=drone_vs_bird_finetune, exist_ok=False, pretrained=True, optimizer=auto, verbose=True, seed=0, deterministic=True, single_cls=False, rect=False, cos_lr=False, close_mosaic=10, resume=False, amp=True, fraction=1.0, profile=False, freeze=None, multi_scale=False, overlap_mask=True, mask_ratio=4, dropout=0.0, val=True, split=val, save_json=False, save_hybrid=False, conf=None, iou=0.7, max_det=300, half=False, dnn=False, plots=True, source=None, vid_stride=1, stream_buffer=False, visualize=False, augment=False, agnostic_nms=False, classes=None, retina_masks=False, embed=None, show=False, save_frames=False, save_txt=False, save_conf=False, save_crop=False, show_labels=True, show_conf=True, show_boxes=True, line_width=None, format=torchscript, keras=False, optimize=False, int8=False, dynamic=False, simplify=True, opset=None, workspace=None, nms=False, lr0=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, warmup_bias_lr=0.1, box=7.5, cls=0.5, dfl=1.5, pose=12.0, kobj=1.0, nbs=64, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, bgr=0.0, mosaic=1.0, mixup=0.0, copy_paste=0.0, copy_paste_mode=flip, auto_augment=randaugment, erasing=0.4, crop_fraction=1.0, cfg=None, tracker=botsort.yaml, save_dir=runs/detect/drone_vs_bird_finetune


