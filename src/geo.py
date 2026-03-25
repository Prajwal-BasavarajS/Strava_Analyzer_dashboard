import sqlite3
import polyline


DB_PATH = "data/processed/strava.db"


def get_first_route():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT activity_id, name, activity_type, summary_polyline
        FROM activities
        WHERE summary_polyline IS NOT NULL
          AND summary_polyline != ''
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    return row


def main():
    row = get_first_route()

    if not row:
        print("No route with summary_polyline found.")
        return

    activity_id, name, activity_type, summary_polyline = row
    coords = polyline.decode(summary_polyline)

    print(f"Activity ID   : {activity_id}")
    print(f"Activity Name : {name}")
    print(f"Activity Type : {activity_type}")
    print(f"Decoded Points: {len(coords)}")

    print("\nFirst 10 coordinates:")
    for i, coord in enumerate(coords[:10], start=1):
        print(f"{i}: {coord}")


if __name__ == "__main__":
    main()