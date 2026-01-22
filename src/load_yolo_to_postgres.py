import os
import json
import psycopg2
from pathlib import Path
from ultralytics import YOLO

# === CONFIG ===
DATA_DIR = Path("data/raw/images")  # folder structure: data/raw/images/<channel_name>/*.jpg
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "newpassword123"
}

# Connect to Postgres
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # make sure the weights file exists
print("YOLOv8n model loaded successfully!")

# Iterate over channels
for channel_dir in DATA_DIR.iterdir():
    if not channel_dir.is_dir():
        continue
    channel_name = channel_dir.name
    print(f"Processing channel: {channel_name}")

    for img_path in channel_dir.glob("*.jpg"):
        results = model(img_path)
        
        # Prepare JSON and bbox text
        for det in results[0].boxes:
            bbox_list = det.xyxy.tolist()[0] if hasattr(det, "xyxy") else det.xyxy
            bbox_text = json.dumps(bbox_list)  # store as text

            # Get message_id: must exist in telegram_messages
            # Here we assume image name encodes message_id: e.g., "CheMed123_11.jpg" -> message_id=11
            message_id = int(img_path.stem.split("_")[-1])

            # Image category: placeholder or logic based on class_id
            image_category = "product_display"

            # Insert into raw_yolo_json
            cur.execute("""
                INSERT INTO raw_yolo_json (
                    message_id, class_id, confidence, bbox, channel_name, image_category, file_name
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    message_id,
                    int(det.cls[0]),  # class_id
                    float(det.conf[0]),  # confidence
                    bbox_text,
                    channel_name,
                    image_category,
                    img_path.name
                )
            )

        conn.commit()
        print(f"Saved predictions for {img_path.name}")

cur.close()
conn.close()
print("YOLO loading to Postgres completed successfully!")
