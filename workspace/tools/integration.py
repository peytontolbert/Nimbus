import requests
import json
import logging
from datetime import datetime, timedelta

class integration:
    def __init__(self):
        self.api_credentials = {}
        self.logger = logging.getLogger("APIIntegrator")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("api_integrator.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.load_credentials()

    def load_credentials(self, file_path="api_credentials.json"):
        """Load API credentials from a secure file."""
        try:
            with open(file_path, "r") as f:
                self.api_credentials = json.load(f)
            self.logger.info("API credentials loaded successfully.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading credentials: {e}")
            self.api_credentials = {}

    def store_credentials(self, api_name: str, credentials: dict, file_path="api_credentials.json"):
        """Store API credentials securely."""
        self.api_credentials[api_name] = credentials
        with open(file_path, "w") as f:
            json.dump(self.api_credentials, f)
        self.logger.info(f"Credentials for {api_name} stored successfully.")

    def authenticate(self, api_name: str, auth_method: str, auth_data: dict) -> dict:
        """Handle authentication for different APIs."""
        if auth_method == "api_key":
            self.store_credentials(api_name, {"api_key": auth_data["api_key"]})
            return {"status": "success", "message": "API key stored."}
        elif auth_method == "oauth":
            response = self.make_post_request(auth_data["auth_url"], auth_data["payload"])
            if "error" not in response:
                self.store_credentials(api_name, {"access_token": response["access_token"]})
                return {"status": "success", "message": "OAuth token stored."}
            else:
                return {"status": "failure", "message": response["error"]}
        else:
            return {"status": "failure", "message": "Unsupported authentication method."}

    def refresh_token(self, api_name: str, refresh_url: str, refresh_payload: dict) -> dict:
        """Refresh the OAuth token."""
        credentials = self.api_credentials.get(api_name)
        if not credentials or "refresh_token" not in credentials:
            return {"error": "Refresh token not found for this API."}
        
        response = self.make_post_request(refresh_url, refresh_payload)
        if "error" not in response:
            self.api_credentials[api_name]["access_token"] = response["access_token"]
            self.store_credentials(api_name, self.api_credentials[api_name])
            return {"status": "success", "message": "Token refreshed successfully."}
        else:
            return {"status": "failure", "message": response["error"]}

    def make_get_request(self, base_url: str, endpoint: str, params: dict = None, headers: dict = None) -> dict:
        """Make a GET request to the specified API."""
        url = f"{base_url}/{endpoint}"
        return self._make_request("GET", url, params=params, headers=headers)

    def make_post_request(self, base_url: str, endpoint: str, payload: dict = None, headers: dict = None) -> dict:
        """Make a POST request to the specified API."""
        url = f"{base_url}/{endpoint}"
        return self._make_request("POST", url, json=payload, headers=headers)

    def make_custom_request(self, method: str, base_url: str, endpoint: str, data: dict = None, headers: dict = None) -> dict:
        """Make a custom HTTP request (e.g., PUT, DELETE)."""
        url = f"{base_url}/{endpoint}"
        return self._make_request(method, url, json=data, headers=headers)

    def _make_request(self, method: str, url: str, **kwargs) -> dict:
        """Helper function to make an HTTP request and handle errors."""
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            self.logger.info(f"Successfully made {method} request to {url}.")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred during {method} request to {url}: {e}")
            return {"error": str(e)}

    def schedule_api_call(self, base_url: str, endpoint: str, interval: int, params: dict = None, headers: dict = None):
        """Schedule an API call at regular intervals."""
        next_call = datetime.now() + timedelta(seconds=interval)
        while True:
            if datetime.now() >= next_call:
                self.make_get_request(base_url, endpoint, params, headers)
                next_call = datetime.now() + timedelta(seconds=interval)
    
    def chain_requests(self, requests_list: list) -> list:
        """Chain multiple API requests together."""
        results = []
        for req in requests_list:
            method = req.get("method", "GET")
            result = self._make_request(method, req["url"], params=req.get("params"), headers=req.get("headers"))
            results.append(result)
            if "error" in result:
                break  # Stop chaining if an error occurs
        return results

    def get_api_status(self, base_url: str) -> dict:
        """Check the status of the API."""
        url = f"{base_url}/status"
        return self._make_request("GET", url)

    def log_api_interaction(self, api_name: str, action: str, response: dict):
        """Log an API interaction for auditing."""
        log_entry = {
            "api_name": api_name,
            "action": action,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"API Interaction Logged: {json.dumps(log_entry)}")
