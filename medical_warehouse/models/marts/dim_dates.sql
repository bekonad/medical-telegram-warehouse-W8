{{ config(materialized='table') }}

SELECT DISTINCT
    TO_CHAR(message_date,'YYYYMMDD')::int AS date_key,
    message_date::date AS full_date,
    EXTRACT(DOW FROM message_date)::int AS day_of_week,
    TO_CHAR(message_date, 'Day') AS day_name,
    EXTRACT(WEEK FROM message_date)::int AS week_of_year,
    EXTRACT(MONTH FROM message_date)::int AS month,
    EXTRACT(QUARTER FROM message_date)::int AS quarter,
    EXTRACT(YEAR FROM message_date)::int AS year,
    CASE WHEN EXTRACT(DOW FROM message_date) IN (0,6) THEN true ELSE false END AS is_weekend
FROM {{ ref('stg_telegram_messages') }}
