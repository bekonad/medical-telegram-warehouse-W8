from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import SessionLocal
from api import schemas, crud

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Task 4 Analytical API powered by dbt marts",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Endpoint 1: Top Products
# -----------------------------
@app.get(
    "/api/reports/top-products",
    response_model=List[schemas.TopProduct],
    description="Returns most frequently mentioned products/terms"
)
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    rows = crud.get_top_products(db, limit)
    return [{"term": r[0], "frequency": r[1]} for r in rows]


# -----------------------------
# Endpoint 2: Channel Activity
# -----------------------------
@app.get(
    "/api/channels/{channel_name}/activity",
    response_model=List[schemas.ChannelActivity],
    description="Returns posting activity trend for a channel"
)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    rows = crud.get_channel_activity(db, channel_name)
    if not rows:
        raise HTTPException(status_code=404, detail="Channel not found")
    return [
        {
            "channel_name": r[0],
            "date": r[1],
            "message_count": r[2]
        }
        for r in rows
    ]


# -----------------------------
# Endpoint 3: Message Search
# -----------------------------
@app.get(
    "/api/search/messages",
    response_model=List[schemas.MessageSearchResult],
    description="Search messages containing a keyword"
)
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    rows = crud.search_messages(db, query, limit)
    return [
        {
            "message_id": r[0],
            "channel_name": r[1],
            "message_text": r[2],
            "message_date": r[3]
        }
        for r in rows
    ]


# -----------------------------
# Endpoint 4: Visual Content Stats
# -----------------------------
@app.get(
    "/api/reports/visual-content",
    response_model=List[schemas.VisualContentStat],
    description="Returns image usage statistics across channels"
)
def visual_content_stats(db: Session = Depends(get_db)):
    rows = crud.get_visual_content_stats(db)
    return [
        {
            "channel_name": r[0],
            "total_images": r[1],
            "avg_confidence": float(r[2]) if r[2] else None
        }
        for r in rows
    ]
