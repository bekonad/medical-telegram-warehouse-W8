from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import psycopg2

# ===============================
# Database Connection
# ===============================

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="newpassword123",
        port=5432
    )

# ===============================
# FastAPI App
# ===============================

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Task 4 Analytics API for Telegram Messages and YOLO Image Detections",
    version="1.0.0"
)

# ===============================
# Pydantic Schemas
# ===============================

class Message(BaseModel):
    message_id: int
    channel_username: str
    text: Optional[str]
    date: str
    views: Optional[int]
    forwards: Optional[int]
    media_type: Optional[str]

class ImageDetection(BaseModel):
    message_id: int
    class_id: int
    confidence: float
    bbox: Optional[str]
    channel_name: Optional[str]
    image_category: Optional[str]
    file_name: Optional[str]

class ChannelAnalytics(BaseModel):
    channel_username: str
    total_messages: int
    avg_views: Optional[float]
    last_message_date: Optional[str]

class DetectionAnalytics(BaseModel):
    image_category: str
    total_detections: int
    avg_confidence: float

# ===============================
# Messages Endpoints
# ===============================

@app.get("/messages", response_model=List[Message])
def get_messages(limit: int = 20):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            message_id,
            channel_username,
            text,
            date,
            views,
            forwards,
            media_type
        FROM telegram_messages
        ORDER BY message_id DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Message(
            message_id=row[0],
            channel_username=row[1],
            text=row[2],
            date=row[3],
            views=row[4],
            forwards=row[5],
            media_type=row[6]
        )
        for row in rows
    ]

# ===============================
# YOLO Image Detections Endpoints
# ===============================

@app.get("/image-detections", response_model=List[ImageDetection])
def get_image_detections(limit: int = 20):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            message_id,
            class_id,
            confidence,
            bbox,
            channel_name,
            image_category,
            file_name
        FROM raw_yolo_json
        ORDER BY confidence DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        ImageDetection(
            message_id=row[0],
            class_id=row[1],
            confidence=row[2],
            bbox=row[3],
            channel_name=row[4],
            image_category=row[5],
            file_name=row[6]
        )
        for row in rows
    ]

# ===============================
# Analytics Endpoints
# ===============================

@app.get("/analytics/channels", response_model=List[ChannelAnalytics])
def channel_analytics():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            channel_username,
            COUNT(*) AS total_messages,
            AVG(views)::numeric(10,2) AS avg_views,
            MAX(date) AS last_message_date
        FROM telegram_messages
        GROUP BY channel_username
        ORDER BY total_messages DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        ChannelAnalytics(
            channel_username=row[0],
            total_messages=row[1],
            avg_views=float(row[2]) if row[2] is not None else None,
            last_message_date=row[3]
        )
        for row in rows
    ]

@app.get("/analytics/image-detections", response_model=List[DetectionAnalytics])
def detection_analytics():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            image_category,
            COUNT(*) AS total_detections,
            AVG(confidence)::numeric(10,4) AS avg_confidence
        FROM raw_yolo_json
        WHERE image_category IS NOT NULL
        GROUP BY image_category
        ORDER BY total_detections DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        DetectionAnalytics(
            image_category=row[0],
            total_detections=row[1],
            avg_confidence=float(row[2])
        )
        for row in rows
    ]
