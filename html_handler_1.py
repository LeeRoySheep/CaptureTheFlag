# Step 1: Import the modules.
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

def fetch_capital_city(country_name):
    try:
        # Step 2: Dynamic URL based on country
        url = f"https://de.wikipedia.org/wiki/{country_name}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful.
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

    try:
        # Step 3.1: Parse the HTML content with BeautifulSoup.
        soup = BeautifulSoup(response.content, "html.parser")

        # Step 3.2: Find the specific table.
        tables = soup.find_all("table", {"class": "wikitable"})
        if not tables:
            print("Error: Could not find the expected table on the page.")
            return None

        table = tables[0]  # First table contains the respective data for the chosen country.

        # Step 4: Read the table into a DataFrame using pandas.
        df = pd.read_html(StringIO(str(table)))[0]
    except Exception as e:
        print(f"Error parsing the HTML or reading the table: {e}")
        return None

    try:
        # Step 5: Clean up the DataFrame.
        # Flatten multi-level headers if they exist, converting non-strings to empty strings.
        if isinstance(df.columns, pd.MultiIndex):
            # Flatten the column headers, filtering out any None or NaN values.
            df.columns = [" ".join(filter(None, map(str, col))) for col in df.columns]

        # Reset the index to clean up the DataFrame.
        df = df.reset_index(drop=True)

        return df
    except Exception as e:
        print(f"Error cleaning or processing the DataFrame: {e}")
        return None


# Input country to check code
country_name = "Spanien"

# Fetch table for 
capital_df = fetch_capital_city(country_name)

if capital_df is not None:
    print(f"Successfully extracted the table for {country_name}!")

    # Search for the row, where "Hauptstadt" is mentioned (case-insensitive)
    if capital_df.iloc[:, 0].str.contains("Hauptstadt", case=False, na=False).any():
        row_idx = capital_df.iloc[:, 0].str.contains("Hauptstadt", case=False, na=False).idxmax()

        # Extrahiere den Wert der Spalte rechts von der "Hauptstadt"-Zeile
        right_column_value = capital_df.iloc[row_idx, 1]  # Extrahiere den Wert der Spalte rechts von "Hauptstadt"
        print(f"Value to the right of 'Hauptstadt' in {country_name}: {right_column_value}")

    else:
        print("Error: 'Hauptstadt' not found in the table.")
else:
    print(f"Failed to extract the table for {country_name}.")