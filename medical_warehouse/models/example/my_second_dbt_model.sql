{{ config(materialized='view') }}

SELECT
    channel_username,
    COUNT(*) AS total_messages,
    AVG(views) AS avg_views,
    MAX(date) AS last_message_date
FROM {{ ref('my_first_dbt_model') }}   -- ✅ no .sql extension
GROUP BY channel_username
ORDER BY total_messages DESC
