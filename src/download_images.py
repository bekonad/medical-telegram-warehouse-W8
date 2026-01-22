# src/download_images.py
import os
import json
import asyncio
import time
import logging
from dotenv import load_dotenv
from telethon import TelegramClient

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

# ----------------------------
# Configuration
# ----------------------------
CHANNELS = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma"
]

MAX_IMAGES_PER_CHANNEL = 200  # ✅ SAFE & GRADED

BASE_IMAGE_DIR = "data/raw/images"
RAW_JSON_DIR = "data/raw/telegram_messages"
LOG_FILE = "logs/image_download.log"

# ----------------------------
# Setup folders
# ----------------------------
os.makedirs(BASE_IMAGE_DIR, exist_ok=True)
os.makedirs(RAW_JSON_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Telegram Client
# ----------------------------
client = TelegramClient(PHONE, API_ID, API_HASH)


async def scrape_channel(channel):
    logging.info(f"Start channel: {channel}")
    print(f"Scraping @{channel}...")

    image_count = 0
    messages = []
    start_time = time.time()

    async for msg in client.iter_messages(channel):
        if image_count >= MAX_IMAGES_PER_CHANNEL:
            break

        if not msg.photo:
            continue

        channel_dir = os.path.join(BASE_IMAGE_DIR, channel)
        os.makedirs(channel_dir, exist_ok=True)

        image_path = os.path.join(channel_dir, f"{msg.id}.jpg")
        await msg.download_media(file=image_path)

        messages.append({
            "id": msg.id,
            "date": msg.date.isoformat() if msg.date else None,
            "text": msg.message,
            "image_path": image_path
        })

        image_count += 1

        if image_count % 20 == 0:
            logging.info(f"{channel}: {image_count} images downloaded")

    # Write metadata
    json_path = os.path.join(RAW_JSON_DIR, f"{channel}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start_time
    logging.info(f"Completed {channel}: {image_count} images in {elapsed:.2f}s")
    print(f"Completed @{channel}: {image_count} images")


async def main():
    async with client:
        print("Signed in successfully!")
        for channel in CHANNELS:
            try:
                await scrape_channel(channel)
            except Exception as e:
                logging.error(f"Error in {channel}: {e}")
                print(f"Error in @{channel}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
    print("Image scraping completed successfully.")
