DROP TABLE IF EXISTS fct_image_detections;

CREATE TABLE fct_image_detections AS
SELECT
    s.message_id,
    c.channel_key,
    d.date_key,
    s.class_id,
    s.confidence,
    s.image_category
FROM stg_image_detections s
LEFT JOIN dim_channels c ON c.channel_name = s.channel_name
LEFT JOIN stg_telegram_messages m ON m.message_id = s.message_id
LEFT JOIN dim_dates d ON d.full_date = m.message_date::date;
