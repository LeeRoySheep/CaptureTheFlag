import wikipediaapi
import random
import re

def get_flags_dict_from_wikipedia():
    """
    Fetches country flag images using Wikipedia API and correctly matches them to country names.
    """
    wiki = wikipediaapi.Wikipedia("Lesheep666", "de")  # Set user agent and language
    page = wiki.page("Liste_der_Nationalflaggen")  # Wikipedia page for national flags

    if not page.exists():
        return {}

    flags = {}

    # Extract links from the page
    links = page.links

    for title, link_page in links.items():
        if title.startswith("Datei:"):  # Flag images are stored under "Datei:"
            # Extract country name by removing "Datei:" and cleaning up the text
            country_name = re.sub(r"(Flagge von |Flag of |Flagge )", "", title.replace("Datei:", "").replace(".svg", "").replace("_", " ")).strip()

            # Construct the correct flag URL from Wikimedia Commons
            flag_url = f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}"

            # Store country-flag pair
            flags[country_name] = flag_url

    return flags

def get_random_flag():
    flags = get_flags_dict_from_wikipedia()
    if not flags:
        return "Could not fetch flags."
    
    country, flag_url = random.choice(list(flags.items()))
    return f"Random Country: {country}\nFlag URL: {flag_url}"

if __name__ == "__main__":
    print(get_random_flag())
