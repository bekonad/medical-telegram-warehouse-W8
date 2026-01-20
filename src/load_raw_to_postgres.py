"""
Task 2 – Load raw Telegram CSV into PostgreSQL
This creates the raw table used by dbt.
"""

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

CSV_PATH = "data/raw/csv/telegram_flat_utf8.csv"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Reading CSV...")
df = pd.read_csv(CSV_PATH)

print("Writing to PostgreSQL...")
df.to_sql(
    "telegram_messages",
    engine,
    schema="public",
    if_exists="replace",
    index=False
)

print("✅ Raw table public.telegram_messages created")
