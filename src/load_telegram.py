import json, os, psycopg2

# Connect to your Postgres database
conn = psycopg2.connect(
    dbname="postgres",  # or "LocalPostgresSQL" if you created that
    user="postgres",
    password="newpassword123",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Ensure table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS telegram_messages (
    id INT,
    date TIMESTAMP,
    text TEXT,
    channel TEXT
)
""")

# Load JSON files from data/raw/telegram_messages
folder = os.path.join("data", "raw", "telegram_messages")
for file in os.listdir(folder):
    channel = file.replace(".json","")
    with open(os.path.join(folder,file),encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cur.execute(
                "INSERT INTO telegram_messages (id, date, text, channel) VALUES (%s,%s,%s,%s)",
                (msg["id"], msg["date"], msg["text"], channel)
            )

conn.commit()
cur.close()
conn.close()
print("✅ Data loaded into Postgres")
