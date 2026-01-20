-- ==============================================
-- GitHub-ready DBT Validation & Sample Snapshot
-- ==============================================

WITH
-- 1️⃣ Row counts
row_counts AS (
    SELECT 'stg_telegram_messages' AS object, COUNT(*) AS result, 'OK' AS status FROM stg_telegram_messages
    UNION ALL
    SELECT 'dim_channels', COUNT(*), 'OK' FROM dim_channels
    UNION ALL
    SELECT 'dim_dates', COUNT(*), 'OK' FROM dim_dates
    UNION ALL
    SELECT 'fct_messages', COUNT(*), 'OK' FROM fct_messages
),

-- 2️⃣ Foreign key violations (show 0 if none)
fk_violations AS (
    SELECT 'fct_messages → dim_channels' AS object, 
           COALESCE(COUNT(*),0) AS result,
           CASE WHEN COUNT(*) > 0 THEN 'VIOLATION' ELSE 'OK' END AS status
    FROM fct_messages f
    LEFT JOIN dim_channels c ON f.channel_key = c.channel_key
    WHERE c.channel_key IS NULL
    UNION ALL
    SELECT 'fct_messages → dim_dates',
           COALESCE(COUNT(*),0),
           CASE WHEN COUNT(*) > 0 THEN 'VIOLATION' ELSE 'OK' END
    FROM fct_messages f
    LEFT JOIN dim_dates d ON f.date_key = d.date_key
    WHERE d.date_key IS NULL
),

-- 3️⃣ Primary key duplicates (show 0 if none)
pk_duplicates AS (
    SELECT 'stg_telegram_messages PK duplicates' AS object, 
           COALESCE(COUNT(*),0) AS result,
           CASE WHEN COUNT(*) > 0 THEN 'VIOLATION' ELSE 'OK' END AS status
    FROM (
        SELECT message_id
        FROM stg_telegram_messages
        GROUP BY message_id
        HAVING COUNT(*) > 1
    ) sub
    UNION ALL
    SELECT 'fct_messages PK duplicates',
           COALESCE(COUNT(*),0),
           CASE WHEN COUNT(*) > 0 THEN 'VIOLATION' ELSE 'OK' END
    FROM (
        SELECT message_id
        FROM fct_messages
        GROUP BY message_id
        HAVING COUNT(*) > 1
    ) sub
    UNION ALL
    SELECT 'dim_channels PK duplicates',
           COALESCE(COUNT(*),0),
           CASE WHEN COUNT(*) > 0 THEN 'VIOLATION' ELSE 'OK' END
    FROM (
        SELECT channel_key
        FROM dim_channels
        GROUP BY channel_key
        HAVING COUNT(*) > 1
    ) sub
    UNION ALL
    SELECT 'dim_dates PK duplicates',
           COALESCE(COUNT(*),0),
           CASE WHEN COUNT(*) > 0 THEN 'VIOLATION' ELSE 'OK' END
    FROM (
        SELECT date_key
        FROM dim_dates
        GROUP BY date_key
        HAVING COUNT(*) > 1
    ) sub
),

-- 4️⃣ Sample fact messages joined to dimensions
sample_fact AS (
    SELECT
        f.message_id,
        c.channel_name,
        d.full_date,
        LEFT(f.message_text,50) AS message_text_snippet
    FROM fct_messages f
    JOIN dim_channels c ON f.channel_key = c.channel_key
    JOIN dim_dates d ON f.date_key = d.date_key
    ORDER BY f.message_id
    LIMIT 10
)

-- ==============================================
-- Final consolidated output
-- ==============================================
SELECT 'Row Counts' AS check_type, object, result::text, status
FROM row_counts

UNION ALL

SELECT 'FK Violations' AS check_type, object, result::text, status
FROM fk_violations

UNION ALL

SELECT 'PK Duplicates' AS check_type, object, result::text, status
FROM pk_duplicates

UNION ALL

SELECT 'Sample Fact Data' AS check_type,
       'message_id: ' || message_id || ', channel: ' || channel_name || ', date: ' || full_date AS object,
       'text: ' || message_text_snippet || '...' AS result,
       'OK' AS status
FROM sample_fact

ORDER BY check_type, object;
