import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Input country to check code and print actions in row 95 and 108
# country_name = "Deutschland"

class CountryInfo:
    def __init__(self, country_name="Deutschland"):
        """Method for creating instances of the class CountryInfo.
        Access the values from outside via country_info_get_capital_city()
        and country_info_get_inhabitants()"""
        self.country_name = country_name
        self.capital_city = None
        self.inhabitants = None
        self.fetch_country_info()
        
    def fetch_country_info(self):
        df = self.fetch_table_with_data()
        if df is not None:
            self.set_capital_city_from_df(df)
            self.set_inhabitants_from_df(df)

    def fetch_table_with_data(self):
        """
        Fetches the Wikipedia page of the country and extracts the first table.
        """
        try:
            url = f"https://de.wikipedia.org/wiki/{self.country_name}"
            response = requests.get(url)
            response.raise_for_status()  # Ensure request was successful

            soup = BeautifulSoup(response.content, "lxml")
            tables = soup.find_all("table", {"class": "wikitable"})

            if not tables:
                raise NameError(f"Error: Could not find the expected table on {self.country_name}'s page.")

            df = pd.read_html(StringIO(str(tables[0])))[0]  # Extract table
            return df
        except Exception as e:
            raise NameError(f"Error fetching the data for {self.country_name}: {e}")

    def set_capital_city_from_df(self, df):
        """
        Extracts and sets the capital from the DataFrame.
        """
        df_string = df.iloc[:, 0].astype(str)

        if df_string.str.contains("Hauptstadt", case=False, na=False).any():
            row_idx = df_string.str.contains("Hauptstadt", case=False, na=False).idxmax()
            self.capital_city = df.iloc[row_idx, 1]
        else:
            raise NameError(f"Error: 'Hauptstadt' not found for {self.country_name}.")

    def set_inhabitants_from_df(self, df):
        """
        Extracts and sets the population from the DataFrame.
        """
        df.iloc[:, 0] = df.iloc[:, 0].astype(str)
        
        if df.iloc[:, 0].str.contains("Einwohnerzahl", case=False, na=False).any():
            row_idx = df.iloc[:, 0].str.contains("Einwohnerzahl", case=False, na=False).idxmax()
            self.inhabitants = df.iloc[row_idx, 1].split(" ")[0]  # Extract first numeric value
        else:
            raise NameError(f"Error: 'Einwohnerzahl' not found for {self.country_name}.")

    def set_capital_city(self, capital_city):
        self.capital_city = capital_city

    def get_capital_city(self):
        return self.capital_city

    def set_inhabitants(self, inhabitants):
        self.inhabitants = inhabitants

    def get_inhabitants(self):
        return self.inhabitants

##delivers 217 capitals with inhabitants in 60 sekonds