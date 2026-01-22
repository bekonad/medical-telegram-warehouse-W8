DROP VIEW IF EXISTS stg_raw_yolo_json;

CREATE VIEW stg_raw_yolo_json AS
SELECT
    message_id::integer,
    class_id::integer,
    confidence::double precision,
    bbox::text,
    channel_name::text,
    image_category::text,
    file_name::text
FROM raw_yolo_json;
