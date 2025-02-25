import requests
from bs4 import BeautifulSoup
import re


class CountryInfo:
    def __init__(self, country_name="Deutschland"):
        """
        Initialize CountryInfo with a given country name and fetch relevant data.
        """
        self.country_name = country_name
        self.capital_city = None
        self.inhabitants = None
        self.fetch_country_info()

    def fetch_country_info(self):
        """
        Fetch Wikipedia page and extract capital city and population.
        """
        url = f"https://de.wikipedia.org/wiki/{self.country_name}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(f"Error fetching data for {self.country_name}. HTTP Status: {response.status_code}")

        soup = BeautifulSoup(response.content, "lxml")

        # Find all tables and scan them for relevant data
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["th", "td"])
                if len(cells) < 2:
                    continue

                header_text = cells[0].get_text(strip=True).lower()

                # Check for "Hauptstadt" (capital city)
                if "hauptstadt" in header_text:
                    self.capital_city = cells[1].get_text(strip=True)

                # Check for "Einwohnerzahl" (population)
                if "einwohner" in header_text:
                    self.inhabitants = self.clean_population(cells[1].get_text(strip=True))

                # Stop searching if both values are found
                if self.capital_city and self.inhabitants:
                    break

    def clean_population(self, population_text):
        """
        Extracts and cleans population data, returning it as an integer.
        """
        numbers = re.findall(r'\d+', population_text)  # Extract only digits
        if numbers:
            return int("".join(numbers))  # Combine and convert to integer
        raise ValueError("No Value for inhabitants in html handler.py")

    def get_capital_city(self):
        """Returns the capital city."""
        return self.capital_city

    def get_inhabitants(self):
        """Returns the population as an integer."""
        return self.inhabitants


# Example Usage:
#country = CountryInfo("Spitzbergen und Jan Mayen")
#print("Capital:", country.get_capital_city())
#print("Population:", country.get_inhabitants())
# gives 233 capitals with inhabitants in 58 sekonds