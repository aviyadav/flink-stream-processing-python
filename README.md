# Flink Stream Processing with Python

A collection of Apache Flink streaming pipelines written in Python (PyFlink) that demonstrate real-time clickstream analysis using event-time windows, watermarks, and stream filtering.

---

## Project Structure

```
flink-stream-processing-python/
│
├── basic_stream.py          # Filter clickstream events by session duration
├── time_window_stream.py    # Count page views per 5-second event-time window
│
├── gen_data.py              # Generate clicks.csv (user, page, timestamp, duration)
├── gen_page_clicks.py       # Generate page_clicks.csv (page, timestamp)
├── gen_user_journeys.py     # Generate user_journeys.csv (user, page, timestamp)
│
├── clicks.csv               # Input for basic_stream.py        [generated]
├── page_clicks.csv          # Input for time_window_stream.py  [generated]
├── user_journeys.csv        # Generated user journey data      [generated]
│
├── pyproject.toml
└── README.md
```

---

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (package manager)
- Java 11 (required by Apache Flink)

---

## Setup

```bash
# Install dependencies
uv sync
```

---

## Pipelines

### 1. Basic Stream — Filter by Session Duration

**Files:** `gen_data.py` → `clicks.csv` → `basic_stream.py`

Each record represents a user visiting a page:

| Field       | Type   | Example        |
|-------------|--------|----------------|
| `user_id`   | string | `user1`        |
| `page`      | string | `/products`    |
| `timestamp` | int    | `1634567890`   |
| `duration`  | int    | `120` (seconds)|

**Generate the data:**

```bash
python gen_data.py
```

This creates `clicks.csv` with 10,000 records across 49 users and 6 pages.

**Run the pipeline:**

```bash
python basic_stream.py
```

Reads `clicks.csv` and prints only the events where the user spent **more than 60 seconds** on a page.

---

### 2. Time Window Stream — Page View Counts

**Files:** `gen_page_clicks.py` → `page_clicks.csv` → `time_window_stream.py`

Each record represents a page view event:

| Field       | Type   | Example      |
|-------------|--------|--------------|
| `page`      | string | `home`       |
| `timestamp` | int    | `1634567890` |

**Generate the data:**

```bash
python gen_page_clicks.py
```

This creates `page_clicks.csv` with 10,000 records. Timestamps advance by 0–3 seconds per event to simulate realistic bursty traffic across many 5-second windows.

**Run the pipeline:**

```bash
python time_window_stream.py
```

Reads `page_clicks.csv` and counts page views per page within **5-second event-time tumbling windows**, using the embedded timestamp for event-time assignment and monotonous watermarks.

Example output:
```
(home, 3)
(products, 2)
(cart, 1)
```

---

### 3. User Journey Data Generator

**File:** `gen_user_journeys.py` → `user_journeys.csv`

Each record represents a step in a user's session:

| Field       | Type   | Example      |
|-------------|--------|--------------|
| `user_id`   | string | `user14`     |
| `page`      | string | `cart`       |
| `timestamp` | int    | `1634567915` |

Users follow realistic weighted page transitions:

| Current Page | Possible Next Pages                                      |
|--------------|----------------------------------------------------------|
| `home`       | products (60%), cart (10%), home (10%), exit (20%)       |
| `products`   | cart (50%), home (20%), products (10%), exit (20%)       |
| `cart`       | checkout (40%), home (30%), products (10%), exit (20%)   |
| `checkout`   | exit (100%)                                              |

This naturally produces both **abandoned cart** sessions (`cart → home`) and **successful checkout** sessions (`cart → checkout`).

**Generate the data:**

```bash
python gen_user_journeys.py
```

This creates `user_journeys.csv` with 1,000 records across 50 unique users.

---

## Dependencies

| Package         | Version  | Purpose                        |
|-----------------|----------|--------------------------------|
| `apache-flink`  | >=2.0.0  | Stream processing runtime      |