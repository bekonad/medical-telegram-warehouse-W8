{{ config(materialized='table') }}

-- Staging model: pulls raw telegram messages into a clean table

SELECT
    message_id,
    date,
    views,
    forwards,
    media_type,
    channel_username
FROM public.telegram_messages
WHERE date IS NOT NULL