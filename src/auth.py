import os
import json
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI", "http://localhost/exchange_token")

SCOPES = "read,activity:read_all"


def build_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "approval_prompt": "force",
        "scope": SCOPES,
    }
    return "https://www.strava.com/oauth/authorize?" + urlencode(params)


def exchange_code_for_token(code):
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }
    response = requests.post(url, data=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def get_athlete(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://www.strava.com/api/v3/athlete",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Missing STRAVA_CLIENT_ID or STRAVA_CLIENT_SECRET in .env")

    print("\nOpen this URL in your browser:\n")
    print(build_auth_url())

    code = input("\nPaste the 'code' from the redirected URL here:\n").strip()

    token_data = exchange_code_for_token(code)

    print("\nSave these in your .env file:\n")
    print(f"STRAVA_ACCESS_TOKEN={token_data['access_token']}")
    print(f"STRAVA_REFRESH_TOKEN={token_data['refresh_token']}")
    print(f"STRAVA_EXPIRES_AT={token_data['expires_at']}")

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/token_response.json", "w") as f:
        json.dump(token_data, f, indent=2)

    athlete = get_athlete(token_data["access_token"])
    print(f"\nYour athlete name: {athlete.get('firstname')} {athlete.get('lastname')}")


if __name__ == "__main__":
    main()