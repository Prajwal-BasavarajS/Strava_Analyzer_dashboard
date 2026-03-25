import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
EXPIRES_AT = os.getenv("STRAVA_EXPIRES_AT")


def refresh_access_token():
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    }
    response = requests.post(url, data=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_activities(page=1, per_page=30):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {
        "page": page,
        "per_page": per_page,
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    if not ACCESS_TOKEN:
        raise ValueError("Missing STRAVA_ACCESS_TOKEN in .env")

    all_activities = []
    page = 1
    per_page = 30

    while True:
        activities = fetch_activities(page=page, per_page=per_page)

        if not activities:
            break

        print(f"Fetched page {page}: {len(activities)} activities")
        all_activities.extend(activities)

        if len(activities) < per_page:
            break

        page += 1
        time.sleep(1)

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/activities.json", "w") as f:
        json.dump(all_activities, f, indent=2)

    print(f"\nSaved {len(all_activities)} activities to data/raw/activities.json")


if __name__ == "__main__":
    main()