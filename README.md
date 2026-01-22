# Medical Telegram Data Warehouse Project (Week 8) 🎯

## Legend of Symbols 🗂️

| Symbol | Meaning |
|--------|---------|
| 📥     | Task 1: Data Scraping and Collection |
| 🛠️     | Task 2: dbt Transformations and Modeling |
| 🖼️     | Task 3: YOLO Image Detection and Enrichment |
| 💾     | Fact Table / Enriched Data Storage |
| 🏛️     | Dimension Table (Channels) |
| 📅     | Dimension Table (Dates) |
| 🏷️     | Detected Objects / Labels |
| ⚡     | Quick Analytics Flow / End-to-End Pipeline |
| 📩     | Telegram Messages Input |
| 🚀     | FastAPI Endpoints / Analytics Outputs |
| ✅     | Validation / Checks Passed |
| ⚙️     | Setup Instructions / Environment Configuration |
| 🏁     | Next Steps / Future Tasks |

---

## Table of Contents

- [Medical Telegram Data Warehouse Project (Week 8) 🎯](#medical-telegram-data-warehouse-project-week-8-)
  - [Legend of Symbols 🗂️](#legend-of-symbols-️)
  - [Table of Contents](#table-of-contents)
  - [Project Objective 🎯](#project-objective-)
  - [Task 1: Data Scraping and Collection 📥](#task-1-data-scraping-and-collection-)
  - [Task 2: Data Modeling and Transformation (dbt) 🛠️](#task-2-data-modeling-and-transformation-dbt-️)
  - [Task 3: Image Data Enrichment (YOLOv8) 🖼️](#task-3-image-data-enrichment-yolov8-️)
  - [Data Warehouse Structure ⭐](#data-warehouse-structure-)
  - [Validation and Snapshot ✅](#validation-and-snapshot-)
  - [Quick Analytics Flow ⚡](#quick-analytics-flow-)
  - [Next Steps 🏁](#next-steps-)
  - [Repository Organization 📂](#repository-organization-)
  - [Setup Instructions ⚙️](#setup-instructions-️)

---

## Project Objective 🎯

The goal of this project is to generate actionable insights about Ethiopian medical businesses from Telegram channels. The platform implements a robust ELT pipeline with:

* **Extract & Load:** Scraping messages and media from Telegram channels.
* **Transform:** dbt-based staging and star schema transformations.
* **Analyze:** FastAPI endpoints and data enrichment with image detection.
* **Data Warehouse:** PostgreSQL database with a clean star schema for analytics.

Key business questions:

* Which channels are most active and what are the top posts?
* What are the price and product trends over time?
* How is visual content distributed across channels?
* What are the posting patterns for different channels?

---

## Task 1: Data Scraping and Collection 📥

**Tools:** Telethon, Python

* Scripts used:
  * `scraper.py` → Scrapes Telegram messages and metadata
  * `download_images.py` → Downloads all media/images for messages
  * `load_raw_to_postgres.py` → Loads raw JSON/message data into PostgreSQL
* Channels included: `CheMed123`, `lobelia4cosmetics`, `tikvahpharma`, and others
* **Data Lake Structure:**

```

data/raw/telegram_messages/YYYY-MM-DD/channel_name.json
data/raw/images/{channel_name}/{message_id}.jpg

```

* Scraped data fields:
  `message_id`, `channel_name`, `message_date`, `message_text`, `has_media`, `image_path`, `views`, `forwards`
* Logging in `logs/` tracks scraping activity and errors.

**Outcome:**
All raw messages and images are stored and loaded into the database, ready for staging and transformation.

---

## Task 2: Data Modeling and Transformation (dbt) 🛠️

**Tools:** dbt v1.11.2, PostgreSQL

* **Staging Models:**
  * `stg_telegram_messages`: cleans raw data, converts types, filters invalid records, calculates `message_length` and `has_image`.

* **Dimension Tables:**
  * `dim_channels`: `channel_key`, `channel_name`, `first_post_date`, `last_post_date`, `total_posts`, `avg_views`
  * `dim_dates`: `date_key`, `full_date`, `day_of_week`, `week_of_year`, `month`, `quarter`, `year`, `is_weekend`

* **Fact Table:**
  * `fct_messages`: `message_id`, `channel_key`, `date_key`, `message_text`, `message_length`, `view_count`, `forward_count`, `has_image`

* **dbt Tests:**
  * Primary key uniqueness, not null checks, and foreign key relationships verified for all tables.

* **Materialization:** All tables configured as `{{ config(materialized='table') }}`.

---

## Task 3: Image Data Enrichment (YOLOv8) 🖼️

**Tools:** YOLOv8 (ultralytics), Python

* **Objective:** Detect objects and product-related visuals in channel images to enrich the data warehouse.
* **Script:** `run_yolo.py`

**YOLOv8 Workflow:**

```

```
[ Raw Images ] 📁
     |
     v
```

┌───────────────┐
│ YOLOv8 Model  │ 🔍
│ (yolov8n.pt)  │
└───────────────┘
|
v
[ Detected Objects ] 🏷️
(object labels, confidence scores)
|
v
┌─────────────────────────┐
│ Merge with Fact Table    │ ➕
│ fct_messages.detected_objects
└─────────────────────────┘
|
v
[ Enriched Fact Table ] 💾

```

**Sample Data:**

| message_id | channel_name      | image_path                  | detected_objects      |
| ---------- | ---------------- | --------------------------- | -------------------- |
| 123        | lobelia4cosmetics | data/raw/images/.../123.jpg | ['lipstick', 'brush'] |
| 124        | CheMed123         | data/raw/images/.../124.jpg | ['vitamin', 'bottle'] |

**Outcome:**  
All images are tagged with objects, allowing visual content analysis and integration with message-level analytics.

---

## Data Warehouse Structure ⭐

```

```
      dim_channels 🏛️         dim_dates 📅
             \                     /
              \                   /
               \                 /
                \               /
             fct_messages 💾 (Fact Table)
             ┌───────────────────────────┐
             │ message_id                │
             │ channel_key               │
             │ date_key                  │
             │ message_text              │
             │ message_length            │
             │ view_count                │
             │ forward_count             │
             │ has_image                 │
             │ detected_objects 🏷️       │
             └───────────────────────────┘
```

````

* Star schema validated; foreign keys and primary keys are clean.
* Sample query joining fact and dimensions:

```sql
SELECT f.message_id, f.message_text, f.detected_objects, c.channel_name, d.full_date
FROM fct_messages f
JOIN dim_channels c ON f.channel_key = c.channel_key
JOIN dim_dates d ON f.date_key = d.date_key
LIMIT 10;
````

---

## Validation and Snapshot ✅

| Check Type    | Object                      | Result | Status |
| ------------- | --------------------------- | ------ | ------ |
| Row Counts    | stg_telegram_messages       | 980    | OK     |
| Row Counts    | dim_channels                | 3      | OK     |
| Row Counts    | dim_dates                   | 78     | OK     |
| Row Counts    | fct_messages                | 980    | OK     |
| FK Violations | fct_messages → dim_channels | 0      | OK     |
| FK Violations | fct_messages → dim_dates    | 0      | OK     |
| PK Duplicates | stg_telegram_messages PK    | 0      | OK     |
| PK Duplicates | fct_messages PK             | 0      | OK     |
| PK Duplicates | dim_channels PK             | 0      | OK     |
| PK Duplicates | dim_dates PK                | 0      | OK     |

> All checks passed; star schema joins work end-to-end. Detected objects successfully integrated into fact table.

---

## Quick Analytics Flow ⚡

```
  [ Telegram Messages ] 📩
             |
             v
  [ YOLOv8 Object Detection ] 🖼️
             |
             v
  [ Enriched Fact Table ] 💾
             |
             v
  [ dbt Transformations ] 🛠️
             |
             v
  [ FastAPI Endpoints ] 🚀
   - Top products & channels
   - Message search
   - Visual statistics
```
🧠 Task 4 — Analytical API (FastAPI)
Objective

Expose the transformed data warehouse through a RESTful API to answer analytical and business questions related to Telegram medical channels.

📦 Tech Stack

FastAPI — REST API framework

SQLAlchemy — Database access layer

PostgreSQL — Data warehouse

dbt — Data modeling (facts & dimensions)

📁 Project Structure
api/
├── main.py        # FastAPI app & routes
├── database.py    # SQLAlchemy engine & session
├── schemas.py     # Pydantic request/response models
├── crud.py        # SQL query logic

🚀 How to Run the API
pip install fastapi uvicorn sqlalchemy psycopg2-binary
uvicorn api.main:app --reload


API will be available at:

http://127.0.0.1:8000


Interactive documentation:

http://127.0.0.1:8000/docs

📊 Implemented Endpoints
1️⃣ Top Products

Returns the most frequently mentioned medical terms/products.

GET /api/reports/top-products?limit=10


Response Example

[
  { "term": "paracetamol", "count": 134 },
  { "term": "amoxicillin", "count": 97 }
]

2️⃣ Channel Activity

Returns posting trends and activity metrics for a specific channel.

GET /api/channels/{channel_name}/activity

3️⃣ Message Search

Searches messages containing a keyword.

GET /api/search/messages?query=paracetamol&limit=20

4️⃣ Visual Content Statistics

Returns statistics about image usage detected by YOLO.

GET /api/reports/visual-content

✅ Features

Data validation using Pydantic schemas

Proper HTTP status codes & error handling

Fully backed by dbt mart tables

Auto-generated OpenAPI documentation

📸 Deliverables

FastAPI application

4 analytical endpoints

API documentation screenshots

Example responses---

## Next Steps 🏁

* Task 4: Analytical FastAPI endpoints (top products, channel activity, message search, visual statistics).
* Task 5: Pipeline orchestration using Dagster for automation.

---

## Repository Organization 📂

```
medical_telegram_warehouse/
├─ data/                  # Raw and processed data
├─ logs/                  # Scraper logs
├─ medical_warehouse/     # dbt project
│  ├─ models/
│  │  ├─ staging/         # Staging models
│  │  └─ marts/           # Dimension & fact tables
│  └─ dbt_project.yml
├─ src/                   # Python scripts: scraper.py, download_images.py, load_raw_to_postgres.py, run_yolo.py
├─ sqlfor_all.sql          # Snapshot queries
└─ README.md
```

---

## Setup Instructions ⚙️

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run dbt
cd medical_warehouse
dbt run
dbt test

# Run YOLO image detection
python src/run_yolo.py
```