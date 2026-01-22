DROP TABLE IF EXISTS fct_messages;

CREATE TABLE fct_messages AS
SELECT
    m.message_id,
    c.channel_key,
    d.date_key,
    m.message_text,
    m.message_length,
    m.view_count,
    m.forward_count,
    m.has_image
FROM stg_telegram_messages m
LEFT JOIN dim_channels c ON c.channel_name = m.channel_name
LEFT JOIN dim_dates d ON d.full_date = m.message_date::date;
