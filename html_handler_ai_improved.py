import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import time


class CountryInfo:
    def __init__(self, country_name='Venezuela', country_list=['Mexiko', 'Deutschland', 'Spanien']):
        """
        Initialize CountryInfo with a given country name.
        """
        self.country_list = country_list
        self.country_name = country_name
        self.capital_city = None
        self.inhabitants = None
        self.country_info_dict = self.fetch_all_countries(self.country_list)
    
    
    async def fetch_all_countries(self, country_list):
        """
        Asynchronously fetches Wikipedia data for all countries in parallel.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [CountryInfo(country).fetch_country_info(session) for country in country_list]
            results = await asyncio.gather(*tasks)

            for i, country in enumerate(country_list):
                if results[i] and results[i].capital_city and results[i].inhabitants:
                    self.set_capital_city(results[i].capital_city)
                    self.set_inhabitants(results[i].inhabitants)
                    self.country_info_dict[country] = {"capital_city": self.get_capital_city, "inhabitants": self.get_inhabitants}
            return self.country_info_dict


    async def fetch_country_info(self, session):
        """
        Asynchronously fetch Wikipedia page and extract capital city & population.
        """
        url = f"https://de.wikipedia.org/wiki/{self.country_name}"
        try:
            async with session.get(url, timeout=5, ssl=False) as response:  # SSL disabled
                if response.status != 200:
                    print(f"❌ Error fetching {self.country_name}: HTTP {response.status}")
                    return None  # Return None for failed requests

                html = await response.text()
                soup = BeautifulSoup(html, "lxml")

                # Scan only the first 3 tables for speed
                for table in soup.find_all("table", limit=3):
                    rows = table.find_all("tr")

                    for row in rows:
                        cells = row.find_all(["th", "td"])
                        if len(cells) < 2:
                            continue  # Skip invalid rows

                        key_text = cells[0].get_text(strip=True).lower()
                        value_text = cells[1].get_text(strip=True)

                        if "hauptstadt" in key_text and not self.capital_city:
                            self.capital_city = self.clean_capital_city(cells[1])

                        if "einwohner" in key_text and not self.inhabitants:
                            self.inhabitants = self.clean_population(value_text)

                        if self.capital_city and self.inhabitants:
                            return self  # Return object with data

        except asyncio.TimeoutError:
            print(f"⏳ Timeout fetching {self.country_name}")
            return None  # Return None on timeout

        return self  # Return even if partially filled

    def clean_population(self, population_text):
        """
        Extracts and cleans population data.
        """
        population_text = re.sub(r'\[.*?\]', '', population_text)

        match_mio = re.search(r'(\d{1,3},\d{1,3})\s*Millionen', population_text)
        if match_mio:
            num_str = match_mio.group(1).replace(",", ".")
            return int(float(num_str) * 1_000_000)

        numbers = re.findall(r'\b\d{1,3}(?:\.\d{3})*\b', population_text)
        cleaned_numbers = [int(num.replace(".", "")) for num in numbers if int(num.replace(".", "")) > 1000]

        return max(cleaned_numbers) if cleaned_numbers else None

    def clean_capital_city(self, capital_element):
        """
        Extracts and cleans the capital city name.
        """
        link = capital_element.find("a")
        return link.get_text(strip=True) if link else capital_element.get_text(strip=True)

    def get_capital_city(self):
        return self.capital_city
    
    def set_capital_city(self, capital_city):
        self.capital_city = capital_city
    

    def get_inhabitants(self):
        return self.inhabitants
    

    def set_inhabitants(self, inhabitants):
        self.inhabitants = inhabitants
