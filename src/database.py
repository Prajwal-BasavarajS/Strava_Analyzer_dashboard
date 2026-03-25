import sqlite3
import json
import os

DB_PATH = "data/processed/strava.db"
ACTIVITIES_JSON = "data/raw/activities.json"


def create_connection():
    os.makedirs("data/processed", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS activities (
        activity_id INTEGER PRIMARY KEY,
        name TEXT,
        activity_type TEXT,
        sport_type TEXT,
        start_date TEXT,
        distance REAL,
        moving_time INTEGER,
        elapsed_time INTEGER,
        total_elevation_gain REAL,
        average_speed REAL,
        max_speed REAL,
        private INTEGER,
        summary_polyline TEXT
    );
    """
    conn.execute(query)
    conn.commit()


def load_activities():
    if not os.path.exists(ACTIVITIES_JSON):
        raise FileNotFoundError(f"{ACTIVITIES_JSON} not found. Run python src/fetch.py first.")
    with open(ACTIVITIES_JSON, "r") as f:
        return json.load(f)


def insert_activities(conn, activities):
    query = """
    INSERT OR REPLACE INTO activities (
        activity_id,
        name,
        activity_type,
        sport_type,
        start_date,
        distance,
        moving_time,
        elapsed_time,
        total_elevation_gain,
        average_speed,
        max_speed,
        private,
        summary_polyline
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    rows = []
    for a in activities:
        rows.append((
            a.get("id"),
            a.get("name"),
            a.get("type"),
            a.get("sport_type"),
            a.get("start_date"),
            a.get("distance"),
            a.get("moving_time"),
            a.get("elapsed_time"),
            a.get("total_elevation_gain"),
            a.get("average_speed"),
            a.get("max_speed"),
            1 if a.get("private") else 0,
            a.get("map", {}).get("summary_polyline")
        ))

    conn.executemany(query, rows)
    conn.commit()


def main():
    conn = create_connection()
    create_table(conn)
    activities = load_activities()
    insert_activities(conn, activities)

    count = conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0]
    print(f"✅ Inserted {count} activities into {DB_PATH}")
    conn.close()


if __name__ == "__main__":
    main()