# src/run_yolo.py
import os
import json
from ultralytics import YOLO
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
IMAGE_ROOT = Path("data/raw/images")
OUTPUT_ROOT = Path("output/yolo")
ANNOTATED_DIR = OUTPUT_ROOT / "annotated"
PRED_DIR = OUTPUT_ROOT / "predictions"

ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)
PRED_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Load YOLO model
# ----------------------------
model = YOLO("yolov8n.pt")
print("YOLOv8n model loaded successfully!")

# ----------------------------
# Run inference
# ----------------------------
for channel_dir in IMAGE_ROOT.iterdir():
    if not channel_dir.is_dir():
        continue

    channel_name = channel_dir.name
    print(f"Processing channel: {channel_name}")

    for img_path in channel_dir.glob("*.jpg"):
        results = model(img_path, conf=0.25)

        # Save annotated image
        annotated_path = ANNOTATED_DIR / f"{channel_name}_{img_path.name}"
        results[0].save(filename=str(annotated_path))

        # Save predictions
        detections = []
        for box in results[0].boxes:
            detections.append({
                "class_id": int(box.cls),
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist()
            })

        pred_file = PRED_DIR / f"{channel_name}_{img_path.stem}.json"
        with open(pred_file, "w") as f:
            json.dump(detections, f, indent=2)

print("Done!")
