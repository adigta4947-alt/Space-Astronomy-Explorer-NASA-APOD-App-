import requests
from datetime import date, timedelta

API_KEY = "DEMO_KEY"  # Replace with your key from api.nasa.gov
BASE_URL = "https://api.nasa.gov/planetary/apod"

def get_today_apod():
    """Fetch today's Astronomy Picture of the Day."""
    try:
        response = requests.get(BASE_URL, params={"api_key": API_KEY}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def get_apod_by_date(apod_date):
    """Fetch APOD for a specific date (format: YYYY-MM-DD)."""
    try:
        response = requests.get(BASE_URL, params={
            "api_key": API_KEY,
            "date": apod_date
        }, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def get_last_30_days():
    """Fetch APODs for the last 30 days."""
    today = date.today()
    start = today - timedelta(days=29)
    try:
        response = requests.get(BASE_URL, params={
            "api_key": API_KEY,
            "start_date": str(start),
            "end_date": str(today)
        }, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []
