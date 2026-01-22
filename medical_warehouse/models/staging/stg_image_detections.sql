DROP VIEW IF EXISTS stg_image_detections;

CREATE VIEW stg_image_detections AS
SELECT
    r.message_id,
    r.class_id,
    r.confidence,
    r.bbox,
    r.channel_name,
    r.image_category
FROM stg_raw_yolo_json r
WHERE r.class_id IS NOT NULL;
