import os
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

    response = requests.post(url, data=payload)
    return response.json()


def get_athlete(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://www.strava.com/api/v3/athlete",
        headers=headers
    )
    return response.json()


def main():
    print("\nStep 1: Open this URL in browser:\n")
    print(build_auth_url())

    code = input("\nStep 2: Paste the 'code' from redirected URL here:\n")

    token_data = exchange_code_for_token(code)
    access_token = token_data["access_token"]

    athlete = get_athlete(access_token)

    print("\n SUCCESS")
    print(f"Your name: {athlete['firstname']} {athlete['lastname']}")


if __name__ == "__main__":
    main()