{{ config(materialized='table') }}

WITH source AS (
    SELECT
        message_id::int,
        channel_username AS channel_name,
        convert_from(text::bytea, 'UTF8') AS message_text,
        date::timestamp AS message_date,
        views::int AS view_count,
        forwards::int AS forward_count,
        CASE WHEN media_type IS NOT NULL THEN true ELSE false END AS has_image,
        length(convert_from(text::bytea, 'UTF8')) AS message_length
    FROM public.telegram_messages
    WHERE text IS NOT NULL
)
SELECT * FROM source
