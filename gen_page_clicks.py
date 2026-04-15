import csv
import random

PAGES = ["home", "products", "cart", "checkout", "about", "settings"]
START_TIMESTAMP = 1634567890  # Unix epoch in seconds
NUM_RECORDS = 10_000
OUTPUT_FILE = "page_clicks.csv"

# Each event advances time by a small random increment (0–3 seconds)
# to simulate realistic click arrival patterns across many 5-second windows.
timestamp = START_TIMESTAMP
rows = []
for _ in range(NUM_RECORDS):
    page = random.choice(PAGES)
    rows.append((page, timestamp))
    timestamp += random.randint(0, 3)

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Generated {NUM_RECORDS} records to '{OUTPUT_FILE}'")
print(f"Timestamp range: {START_TIMESTAMP} → {timestamp - 1}")
print(f"Time span: ~{(timestamp - START_TIMESTAMP) / 60:.1f} minutes")
