import requests
import datetime
import time

class message:
    def __init__(self):
        pass

    def message_creator(self, string):
        try:
            print("Message to creator:")
            print(string)
            string_string = str(string)
            data = {"user": "Buddy", "message": string_string}
            response = requests.post(
                "http://localhost:5000/messagetocreator", json=data
            )
            if response.status_code == 200:
                print("Message sent successfully")
            else:
                print("Failed to send message, status code: ", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def message_finn(self, string):
        try:
            print("Message to finn:")
            print(string)
            string_string = str(string)
            data = {"user": "Buddy", "message": string_string}
            response = requests.post("http://localhost:5000/messagetofinn", json=data)
            if response.status_code == 200:
                print("Message sent successfully")
            else:
                print("Failed to send message, status code: ", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def read_chat(self):
        try:
            print("Reading chat....")
            response = requests.get("http://localhost:5000/chat")
            print(response.text)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def read_dm(self):
        try:
            print("Reading private messages....")
            response = requests.get("http://localhost:5000/buddydm")
            print(response.text)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def post_chat(self, string):
        try:
            string_string = str(string)
            data = {"user": "Buddy", "message": string_string}
            response = requests.post("http://localhost:5000/chat", json=data)
            if response.status_code == 200:
                print("Message sent successfully")
            else:
                print("Failed to send message, status code: ", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")



    def message_scheduler(self, recipient: str, message: str, send_time: datetime):
        """
        This tool allows you to schedule messages to be sent at a later time. You can specify the recipient, the message content, and the exact date and time for the message to be sent.
        """
        try:
            current_time = datetime.now()
            delay = (send_time - current_time).total_seconds()
            if delay > 0:
                print(f"Scheduling message to {recipient} in {delay} seconds.")
                time.sleep(delay)
            self.post_chat(f"Message to {recipient}: {message}")
            print(f"Message sent to {recipient} at {send_time}.")
        except Exception as e:
            print(f"An error occurred while scheduling message: {str(e)}")

    def message_archiver(self, message_ids: list):
        """
        This tool enables you to archive old messages to keep your messaging interface clean and organized. You can select specific messages or entire conversations to archive.
        """
        try:
            data = {"message_ids": message_ids}
            response = requests.post("http://localhost:5000/archive_messages", json=data)
            if response.status_code == 200:
                print("Messages archived successfully")
            else:
                print("Failed to archive messages, status code: ", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def message_search(self, query: str):
        """
        This tool helps you search through your messages using keywords or phrases. It returns a list of messages that match your search criteria.
        """
        try:
            params = {"query": query}
            response = requests.get("http://localhost:5000/search_messages", params=params)
            if response.status_code == 200:
                search_results = response.json()
                print(f"Search results for '{query}':")
                for result in search_results:
                    print(result)
                return search_results
            else:
                print("Failed to search messages, status code: ", response.status_code)
                return []
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []

    def message_translator(self, message_id: str, target_language: str):
        """
        This tool automatically translates messages into your preferred language. It supports multiple languages and can be used to translate both incoming and outgoing messages.
        """
        try:
            data = {"message_id": message_id, "target_language": target_language}
            response = requests.post("http://localhost:5000/translate_message", json=data)
            if response.status_code == 200:
                translated_message = response.json().get("translated_message")
                print(f"Translated message: {translated_message}")
                return translated_message
            else:
                print("Failed to translate message, status code: ", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def message_auto_responder(self, auto_response: str, active_times: list):
        """
        This tool sets up automatic responses to incoming messages when you are unavailable. You can customize the auto-response and set specific times for it to be active.
        """
        try:
            data = {"auto_response": auto_response, "active_times": active_times}
            response = requests.post("http://localhost:5000/auto_responder", json=data)
            if response.status_code == 200:
                print("Auto-responder set up successfully")
            else:
                print("Failed to set up auto-responder, status code: ", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None