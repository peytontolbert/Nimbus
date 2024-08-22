import requests


class MessageHandler:
    def __init__(self, api_url):
        self.api_url = api_url

    def check_for_messages(self):
        try:
            response = requests.get(f"{self.api_url}/messages")
            if response.status_code == 200:
                messages = response.json()
                if messages:
                    return messages[0]  # Return the first message for processing
            return None
        except requests.RequestException as e:
            print(f"Error fetching messages: {e}")
            return None
