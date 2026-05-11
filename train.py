from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="dataset/data.yaml",
    epochs=80,
    imgsz=640,
    batch=4,
    device="cpu",
    name="ergo_switch",

    # 🔴 IMPORTANT: Disable color augmentation
    hsv_h=0.0,
    hsv_s=0.0,
    hsv_v=0.0,

    # Optional but recommended (reduce distortion)
    degrees=0.0,
    translate=0.0,
    scale=0.0,
    shear=0.0,
    perspective=0.0,

    # Keep flip if orientation doesn't matter
    flipud=0.0,
    fliplr=0.0,

    # Mosaic can sometimes hurt color tasks
    mosaic=0.0,
    mixup=0.0
)