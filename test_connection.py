
import requests
from config.settings import APOLLO_API_KEY, APOLLO_BASE_URL 
def test_apollo_connection():
 
    if not APOLLO_API_KEY:
        print("API Key missing! Check .env file.")
        return

    url = f"{APOLLO_BASE_URL}/auth/health"

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "x-api-key": APOLLO_API_KEY
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 200:
            print("Apollo API Connected Successfully!")
        else:
            print("API request failed.")

    except requests.exceptions.RequestException as error:
        print("Error:", error)


if __name__ == "__main__":
    test_apollo_connection()
 