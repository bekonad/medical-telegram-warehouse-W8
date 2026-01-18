# scripts/task1_scraper.py
# Task 1: Working Scraper + Populated Data Lake
# Author: Bereket Feleke
# Date: December 30, 2025
# Beginner-friendly: Run this script to scrape Telegram medical channels and save to data lake

import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd
import asyncio

# Load secrets from .env
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

# Folders
RAW_JSON_DIR = "data/raw/json"
RAW_CSV_DIR = "data/raw/csv"
LOGS_DIR = "data/raw/logs"

os.makedirs(RAW_JSON_DIR, exist_ok=True)
os.makedirs(RAW_CSV_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Channels to scrape (from your message)
channels = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma"
]

async def scrape_channel(client, channel_username, limit=500):
    print(f"Scraping channel: {channel_username} (max {limit} messages)")
    
    try:
        entity = await client.get_entity(channel_username)
    except Exception as e:
        print(f"Error getting entity for {channel_username}: {e}")
        return []

    messages = []
    async for message in client.iter_messages(entity, limit=limit):
        msg_data = {
            'message_id': message.id,
            'date': message.date.isoformat() if message.date else None,
            'text': message.message or "",
            'views': message.views or 0,
            'forwards': message.forwards or 0,
            'media_type': message.media.__class__.__name__ if message.media else "None",
            'channel_username': channel_username
        }
        messages.append(msg_data)
    
    print(f"Scraped {len(messages)} messages from {channel_username}")
    return messages

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    
    try:
        await client.start(phone=phone)
        print("Logged in successfully!")
    except SessionPasswordNeededError:
        password = input("Two-step verification enabled. Please enter password: ")
        await client.sign_in(password=password)
        print("Logged in with password!")
    except Exception as e:
        print(f"Login error: {e}")
        return

    all_messages = []

    for channel in tqdm(channels, desc="Scraping channels"):
        messages = await scrape_channel(client, channel, limit=500)  # adjust limit for more data
        all_messages.extend(messages)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save raw JSON
    json_path = os.path.join(RAW_JSON_DIR, f"telegram_raw_{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_messages, f, ensure_ascii=False, indent=2)
    print(f"Saved raw JSON: {json_path}")

    # Save flattened CSV
    df = pd.DataFrame(all_messages)
    csv_path = os.path.join(RAW_CSV_DIR, f"telegram_flat_{timestamp}.csv")
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Saved CSV: {csv_path}")

    # Log summary
    summary = {
        "timestamp": timestamp,
        "total_messages": len(all_messages),
        "channels_scraped": channels,
        "json_file": json_path,
        "csv_file": csv_path
    }
    log_path = os.path.join(LOGS_DIR, f"scrape_summary_{timestamp}.json")
    with open(log_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Log saved: {log_path}")

    print("Task 1 complete! Data lake populated in data/raw/")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())