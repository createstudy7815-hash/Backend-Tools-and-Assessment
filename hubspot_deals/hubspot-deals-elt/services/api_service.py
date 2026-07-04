import requests
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

from loki_logger import get_logger, log_api_call


class APIService:
    """
    HubSpot Deals API Service
    """

    def __init__(
        self,
        base_url: str = "https://api.hubapi.com",
        test_delay_seconds: float = 0,
    ):
        self.base_url = base_url.rstrip("/")
        self.test_delay_seconds = test_delay_seconds
        self.logger = get_logger(__name__)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "HubSpot-Deals-Extractor/1.0",
            }
        )

    def set_access_token(self, token: str):
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}"
            }
        )

    def get_data(
        self,
        access_token: str,
        limit: int = 100,
        after: Optional[str] = None,
        properties: Optional[list] = None,
    ) -> Dict[str, Any]:

        start = datetime.utcnow()

        self.set_access_token(access_token)

        if self.test_delay_seconds > 0:
            time.sleep(self.test_delay_seconds)

        params = {
            "limit": min(limit, 100),
        }

        if after:
            params["after"] = after

        if properties:
            params["properties"] = ",".join(properties)

        url = f"{self.base_url}/crm/v3/objects/deals"

        try:

            response = self.session.get(url, params=params)

            if response.status_code == 429:

                retry = int(response.headers.get("Retry-After", 10))

                self.logger.warning(
                    f"Rate limited. Sleeping {retry} seconds..."
                )

                time.sleep(retry)

                response = self.session.get(url, params=params)

            response.raise_for_status()

            duration = (
                datetime.utcnow() - start
            ).total_seconds() * 1000

            log_api_call(
                self.logger,
                "hubspot_get_deals",
                method="GET",
                status_code=response.status_code,
                duration_ms=round(duration, 2),
            )

            return response.json()

        except requests.exceptions.RequestException as e:

            duration = (
                datetime.utcnow() - start
            ).total_seconds() * 1000

            log_api_call(
                self.logger,
                "hubspot_get_deals",
                method="GET",
                status_code=getattr(e.response, "status_code", 500),
                duration_ms=round(duration, 2),
            )

            self.logger.error(str(e))

            raise

    def validate_token(self, access_token: str) -> bool:

        self.set_access_token(access_token)

        url = f"{self.base_url}/crm/v3/objects/deals"

        try:

            response = self.session.get(
                url,
                params={"limit": 1},
            )

            return response.status_code == 200

        except requests.exceptions.RequestException:

            return False

    def get_account_info(
        self,
        access_token: str,
    ) -> Optional[Dict[str, Any]]:

        self.set_access_token(access_token)

        url = (
            f"{self.base_url}/account-info/v3/details"
        )

        try:

            response = self.session.get(url)

            if response.status_code == 200:
                return response.json()

            return None

        except requests.exceptions.RequestException:

            return None

    def test_connection(
        self,
        access_token: str,
    ) -> Dict[str, Any]:

        result = {
            "token_valid": False,
            "api_reachable": False,
            "data_accessible": False,
            "account_info": None,
            "error": None,
        }

        try:

            valid = self.validate_token(access_token)

            result["token_valid"] = valid
            result["api_reachable"] = valid

            if valid:

                result["account_info"] = self.get_account_info(
                    access_token
                )

                self.get_data(
                    access_token,
                    limit=1,
                )

                result["data_accessible"] = True

        except Exception as e:

            result["error"] = str(e)

        return result