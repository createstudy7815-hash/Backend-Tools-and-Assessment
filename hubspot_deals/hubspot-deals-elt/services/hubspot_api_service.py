import os
import requests
import logging
import time

logging.basicConfig(level=logging.INFO)

class HubSpotAPIService:

    def __init__(self):
        self.access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.base_url = "https://api.hubapi.com"
        self.timeout = int(os.getenv("HUBSPOT_API_TIMEOUT", 30))

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def validate_credentials(self):
        url = f"{self.base_url}/crm/v3/objects/deals?limit=1"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.timeout
        )

        return response.status_code == 200

    def get_deals(self, limit=100, after=None):

        url = f"{self.base_url}/crm/v3/objects/deals"

        params = {"limit": limit}

        if after:
            params["after"] = after

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 429:
                logging.warning("Rate limit exceeded. Waiting 10 seconds...")
                time.sleep(10)
                return self.get_deals(limit, after)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logging.error(f"HubSpot API Error: {e}")
            return None