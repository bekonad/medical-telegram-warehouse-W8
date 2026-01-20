# Medical Telegram Data Warehouse Project (Week 8)

This repository contains a full **ETL/ELT pipeline** for collecting, storing, and analyzing Telegram messages from Ethiopian medical and cosmetic channels. The project demonstrates data scraping, dbt transformations, star schema design, and integrity checks, aligned with the Week 8 KAIM rubric.
=======
>>>>>>> e00c73ac96a6e23f4e161f12366199200cb8549f


## Table of Contents
- [Medical Telegram Data Warehouse Project (Week 8)](#medical-telegram-data-warehouse-project-week-8)
- [This repository contains a full **ETL/ELT pipeline** for collecting, storing, and analyzing Telegram messages from Ethiopian medical and cosmetic channels. The project demonstrates data scraping, dbt transformations, star schema design, and integrity checks, aligned with the Week 8 KAIM rubric.](#this-repository-contains-a-full-etlelt-pipeline-for-collecting-storing-and-analyzing-telegram-messages-from-ethiopian-medical-and-cosmetic-channels-the-project-demonstrates-data-scraping-dbt-transformations-star-schema-design-and-integrity-checks-aligned-with-the-week-8-kaim-rubric)
  - [Table of Contents](#table-of-contents)
  - [Project Objective](#project-objective)
  - [Task 1: Data Scraping and Collection](#task-1-data-scraping-and-collection)
  - [Task 2: Data Modeling and Transformation (dbt)](#task-2-data-modeling-and-transformation-dbt)
  - [Data Warehouse Structure](#data-warehouse-structure)
  - [Validation and Snapshot](#validation-and-snapshot)
  - [Next Steps](#next-steps)
  - [Repository Organization](#repository-organization)
  - [Setup Instructions](#setup-instructions)
  - [\<\<\<\<\<\<\< HEAD](#-head)
- [Push branch](#push-branch)
- [Merge into main](#merge-into-main)

---

## Project Objective
The goal of this project is to generate actionable insights about Ethiopian medical businesses from Telegram channels. The platform implements a robust ELT pipeline with:

- **Extract & Load:** Scraping messages and media from Telegram channels.
- **Transform:** dbt-based staging and star schema transformations.
- **Analyze:** FastAPI endpoints and data enrichment with image detection (future tasks).
- **Data Warehouse:** PostgreSQL database with a clean star schema for analytics.

Key business questions:
- Most active channels and top posts
- Price and product trends
- Visual content distribution
- Posting patterns over time

---

## Task 1: Data Scraping and Collection
**Tools:** Telethon, Python  

- Scraper script located at: `src/scraper.py` (extracts messages and media)  
- Channels included: `CheMed123`, `lobelia4cosmetics`, `tikvahpharma`, and additional channels  
- **Data Lake Structure:**
```

data/raw/telegram_messages/YYYY-MM-DD/channel_name.json
data/raw/images/{channel_name}/{message_id}.jpg

```
- Scraped data fields:  
`message_id`, `channel_name`, `message_date`, `message_text`, `has_media`, `image_path`, `views`, `forwards`  
- Logging in `logs/` tracks scraping activity and error handling.

**Outcome:**  
All raw messages are successfully stored, including images, ready for staging and transformation.

---

## Task 2: Data Modeling and Transformation (dbt)
**Tools:** dbt v1.11.2, PostgreSQL  

- **Staging Models:**  
- `stg_telegram_messages`: cleans raw data, converts types, filters invalid records, calculates `message_length` and `has_image`.  

- **Dimension Tables:**  
- `dim_channels`: `channel_key`, `channel_name`, `first_post_date`, `last_post_date`, `total_posts`, `avg_views`  
- `dim_dates`: `date_key`, `full_date`, `day_of_week`, `week_of_year`, `month`, `quarter`, `year`, `is_weekend`  

- **Fact Table:**  
- `fct_messages`: `message_id`, `channel_key`, `date_key`, `message_text`, `message_length`, `view_count`, `forward_count`, `has_image`  

- **dbt Tests:**  
- Primary key uniqueness, not null checks, and foreign key relationships verified for all tables.  

- **Materialization:** All tables configured as `{{ config(materialized='table') }}`.

---

## Data Warehouse Structure

```

```
     dim_channels        dim_dates
          \                 /
           \               /
            \             /
             \           /
              fct_messages (fact table)
```

````

- Star schema validated; foreign keys and primary keys are clean.  
- Sample query joining fact and dimensions:

```sql
SELECT f.message_id, f.message_text, c.channel_name, d.full_date
FROM fct_messages f
JOIN dim_channels c ON f.channel_key = c.channel_key
JOIN dim_dates d ON f.date_key = d.date_key
LIMIT 10;
````

---

## Validation and Snapshot

The following SQL snapshot checks the integrity of all tables and provides a sample of fact data.

**Key checks included:**

* Row counts per table
* Foreign key violations
* Primary key duplicates
* Sample messages joined to dimensions

| Check Type       | Object                                                      | Result                        | Status |
| ---------------- | ----------------------------------------------------------- | ----------------------------- | ------ |
| Row Counts       | stg_telegram_messages                                       | 980                           | OK     |
| Row Counts       | dim_channels                                                | 3                             | OK     |
| Row Counts       | dim_dates                                                   | 78                            | OK     |
| Row Counts       | fct_messages                                                | 980                           | OK     |
| FK Violations    | fct_messages → dim_channels                                 | 0                             | OK     |
| FK Violations    | fct_messages → dim_dates                                    | 0                             | OK     |
| PK Duplicates    | stg_telegram_messages PK                                    | 0                             | OK     |
| PK Duplicates    | fct_messages PK                                             | 0                             | OK     |
| PK Duplicates    | dim_channels PK                                             | 0                             | OK     |
| PK Duplicates    | dim_dates PK                                                | 0                             | OK     |
| Sample Fact Data | message_id: 1, channel: CheMed123, date: 2022-09-05         | text: Example text snippet... | OK     |
| Sample Fact Data | message_id: 2, channel: lobelia4cosmetics, date: 2022-09-06 | text: Example text snippet... | OK     |
| …                | …                                                           | …                             | …      |

> All checks passed; foreign keys and primary keys are clean. Sample data confirms the star schema joins work end-to-end.

---

## Next Steps

* **Task 3:** Data enrichment with YOLOv8 object detection for images.
* **Task 4:** Analytical FastAPI endpoints (top products, channel activity, message search, visual statistics).
* **Task 5:** Pipeline orchestration using Dagster for automation.

---

## Repository Organization

```
medical_telegram_warehouse/
├─ data/                  # Raw and processed data
├─ logs/                  # Scraper logs
├─ medical_warehouse/     # dbt project
│  ├─ models/
│  │  ├─ staging/         # Staging models
│  │  └─ marts/           # Dimension & fact tables
│  └─ dbt_project.yml
├─ src/                   # Python scripts (scraper, loaders)
├─ sqlfor all.sql          # Snapshot queries
└─ README.md
```

* `.gitignore` excludes `.env`, virtual environments, large files, and `__pycache__`.
* `requirements.txt` contains Python dependencies.

---

## Setup Instructions

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
```

<<<<<<< HEAD
---
=======
# Push branch
git push origin task-2

# Merge into main
git checkout main
git merge task-2
git push origin main
```
>>>>>>> e00c73ac96a6e23f4e161f12366199200cb8549f
