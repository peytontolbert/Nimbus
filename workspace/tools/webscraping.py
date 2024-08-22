import requests
from bs4 import BeautifulSoup

class webscraping:
    def __init__(self):
        pass

    def dataextractor(self, url: str, selector: str, method: str):
        """
        A tool for extracting data from web pages.

        Args:
            url (str): The URL of the web page to scrape.
            selector (str): The CSS selector to find elements.
            method (str): The method to extract data ('text' or 'html').

        Returns:
            list: A list of extracted data from the web page.
        """
        # Check user permission
        if not self._user_permission():
            raise PermissionError("User permission required to perform web scraping.")

        # Fetch the web page
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve the web page. Status code: {response.status_code}")

        # Parse the web page content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data based on the selector and method
        elements = soup.select(selector)
        if method == 'text':
            return [element.get_text() for element in elements]
        elif method == 'html':
            return [str(element) for element in elements]
        else:
            raise ValueError("Invalid method. Use 'text' or 'html'.")

    def _user_permission(self):
        """
        Simulate a check for user permission to perform web scraping.

        Returns:
            bool: True if the user has given permission, False otherwise.
        """
        # In a real-world scenario, this would involve checking user consent.
        # Here, we simulate permission being always granted for demonstration purposes.
        return True