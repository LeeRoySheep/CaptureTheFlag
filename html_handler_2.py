import requests
from bs4 import BeautifulSoup
import re  # For extracting numbers


class CountryInfo:
    def __init__(self, country_name="Deutschland"):
        '''
        standard constructor for CountryInfo class initializing a object with given
        country name and fetches capital city as string and inhabitants as int value
        '''
        self.country_name = country_name
        self.capital_city = None
        self.inhabitants = None
        self.fetch_country_info()

    def fetch_country_info(self):
        """
        function to create set capital_city as string a
        """
        url = f"https://de.wikipedia.org/wiki/{self.country_name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Error fetching data for {self.country_name}. Status Code: {response.status_code}")

        soup = BeautifulSoup(response.content, "lxml") # is supposed to be quicker than html_parser
        tables = soup.find_all("table")  # Find all tables on the page

        for table in tables:
            rows = table.find_all("tr")

            for row in rows:
                headers = row.find_all("td", class_="ibleft")  # Look for the 'ibleft' class
                if headers:
                    key = headers[0].get_text(strip=True)  # Extract the header text
                    if len(row.find_all("td")) > 1:
                        data_cell = row.find_all("td")[1] 
                    else:
                        raise NameError("Cannot find wanted name marks in html to extract data!")

                    if data_cell:
                        value = data_cell.get_text(strip=True)

                        if "Hauptstadt" in key:
                            self.set_capital_city(value)
                        elif "Einwohner" in key:
                            self.set_inhabitants(self.clean_population(value))

    def clean_population(self, population_text):
        """
        Extracts and cleans population data and returning it as integer.
        """
        numbers = re.findall(r'\d+', population_text)  # Extract only digits
        if numbers:
            return int("".join(numbers))  # Combine and convert to integer
        raise ValueError("No value found for inhabitants!")

    def get_capital_city(self):
        '''
        standard getter funktion to call capital_city string variable
        and inhabitatns variable from CountryInfo object may raise NameError
        '''
        return self.capital_city

    def get_inhabitants(self):
        '''
        standard getter for inhabitants variable may raise value or even name error
        '''
        return self.inhabitants
    

    def set_capital_city(self, capital_city):
        """
        function to set class variable capital_city as string
        might raise TypeError
        """
        if type(capital_city) != str:
            raise TypeError("Capital_city must be from type String line 79")
    

    def set_inhabitants(self, inhabitants):
        """
        function to set class variable inhabitants with non negative in value
        raises TupeError for no integer input and ValueError for negative inputs
        """
        if type(inhabitants) != int:
            raise TypeError("The inhabitants must be from type int! line 88")
        elif inhabitants <= 0:
            raise ValueError("The inhabitants mus be a non negative numver bigger than 0!")
        self.inhabitants = inhabitants

