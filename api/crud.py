from sqlalchemy.orm import Session
from sqlalchemy import text


# Endpoint 1: Top Products (term frequency)
def get_top_products(db: Session, limit: int):
    query = text("""
        SELECT
            LOWER(word) AS term,
            COUNT(*) AS frequency
        FROM (
            SELECT
                unnest(string_to_array(message_text, ' ')) AS word
            FROM fct_messages
            WHERE message_text IS NOT NULL
        ) t
        WHERE length(word) > 4
        GROUP BY term
        ORDER BY frequency DESC
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).fetchall()


# Endpoint 2: Channel Activity
def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT
            c.channel_name,
            d.full_date::text,
            COUNT(*) AS message_count
        FROM fct_messages f
        JOIN dim_channels c ON f.channel_key = c.channel_key
        JOIN dim_dates d ON f.date_key = d.date_key
        WHERE c.channel_name = :channel
        GROUP BY c.channel_name, d.full_date
        ORDER BY d.full_date
    """)
    return db.execute(query, {"channel": channel_name}).fetchall()


# Endpoint 3: Message Search
def search_messages(db: Session, query_text: str, limit: int):
    query = text("""
        SELECT
            f.message_id,
            c.channel_name,
            f.message_text,
            d.full_date::text
        FROM fct_messages f
        JOIN dim_channels c ON f.channel_key = c.channel_key
        JOIN dim_dates d ON f.date_key = d.date_key
        WHERE f.message_text ILIKE :query
        ORDER BY d.full_date DESC
        LIMIT :limit
    """)
    return db.execute(
        query,
        {"query": f"%{query_text}%", "limit": limit}
    ).fetchall()


# Endpoint 4: Visual Content Stats
def get_visual_content_stats(db: Session):
    query = text("""
        SELECT
            c.channel_name,
            COUNT(*) AS total_images,
            AVG(f.confidence)::numeric(10,4) AS avg_confidence
        FROM fct_image_detections f
        JOIN dim_channels c ON f.channel_key = c.channel_key
        GROUP BY c.channel_name
        ORDER BY total_images DESC
    """)
    return db.execute(query).fetchall()
