
import requests
from config.settings import APOLLO_API_KEY, APOLLO_BASE_URL


class ApolloClient:

    def __init__(self):

        if not APOLLO_API_KEY:
            raise ValueError("Apollo API Key is missing in .env file")

        self.base_url = APOLLO_BASE_URL.rstrip("/")

        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "x-api-key": APOLLO_API_KEY
        }

    def request(self, method, endpoint, params=None, json_data=None):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=30
            )

            response.raise_for_status()

            if response.status_code == 204:
                return {}

            return response.json()

        except requests.exceptions.HTTPError as error:
            print("Apollo API HTTP Error:", error)
            print("Response:", response.text)
            raise

        except requests.exceptions.RequestException as error:
            print("Apollo API Connection Error:", error)
            raise

    def health_check(self):

        return self.request(
            "GET",
            "auth/health"
        )

    def search_companies(self, filters):

        return self.request(
            "POST",
            "mixed_companies/search",
            json_data=filters
        )

    def search_employees(self, filters):

        return self.request(
            "POST",
            "mixed_people/api_search",
            json_data=filters
        )

    def bulk_enrichment(self, people):

        return self.request(
            "POST",
            "people/bulk_match",
            json_data=people
        )
 