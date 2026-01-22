DROP TABLE IF EXISTS stg_telegram_messages;

CREATE TABLE stg_telegram_messages AS
SELECT
    message_id::integer,
    channel_username AS channel_name,
    text AS message_text,
    date::timestamp AS message_date,
    views::integer AS view_count,
    forwards::integer AS forward_count,
    CASE WHEN media_type IS NOT NULL AND media_type <> '' THEN true ELSE false END AS has_image,
    LENGTH(text) AS message_length
FROM telegram_messages;
