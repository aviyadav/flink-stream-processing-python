import csv
import random

OUTPUT_FILE = "user_journeys.csv"
NUM_RECORDS = 10000
START_TIMESTAMP = 1634567890  # Base Unix timestamp (seconds)

# Realistic page transition probabilities modelling user journeys.
# Each entry is (next_page, weight). A None next_page means the session ends.
PAGE_TRANSITIONS = {
    "home": [("products", 60), ("cart", 10), ("home", 10), (None, 20)],
    "products": [("cart", 50), ("home", 20), ("products", 10), (None, 20)],
    "cart": [("checkout", 40), ("home", 30), ("products", 10), (None, 20)],
    "checkout": [(None, 100)],  # Session always ends after checkout
}

NUM_USERS = 50
users = [f"user{i}" for i in range(1, NUM_USERS + 1)]


def weighted_choice(options):
    """Pick a next_page from a list of (page, weight) tuples."""
    choices, weights = zip(*options)
    return random.choices(choices, weights=weights, k=1)[0]


def simulate_journey(user_id, start_ts):
    """
    Simulate one user session starting from 'home'.
    Returns a list of (user_id, page, timestamp) tuples.
    Each page visit is 5–30 seconds after the previous one.
    """
    events = []
    page = "home"
    ts = start_ts

    while page is not None:
        events.append((user_id, page, ts))
        ts += random.randint(5, 30)  # Time spent on the current page
        page = weighted_choice(PAGE_TRANSITIONS[page])

    return events


# Build records by simulating journeys until we have >= NUM_RECORDS rows.
records = []
ts = START_TIMESTAMP

while len(records) < NUM_RECORDS:
    user = random.choice(users)
    journey = simulate_journey(user, ts)
    records.extend(journey)
    ts += random.randint(1, 10)  # Small gap between sessions

# Trim to exactly NUM_RECORDS and sort by timestamp for realism.
records = sorted(records[:NUM_RECORDS], key=lambda r: r[2])

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(records)

print(f"Generated {len(records)} records to '{OUTPUT_FILE}'")
print(f"Users      : {NUM_USERS} unique users")
print(f"Timestamp  : {records[0][2]} → {records[-1][2]}")
