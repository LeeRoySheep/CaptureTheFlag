import requests
import re
from PIL import Image
from io import BytesIO

 


REGEX_URL = re.compile(
                    r'upload\.wikimedia\.org'
                   + r'/wikipedia/commons/thumb/[\w\d]/[\w\d][\w\d]/F\w*\.'
                   + r'svg/120px-F\w*\.svg\.png'
                   )

REGEX_COUNTRY = re.compile(r"tion\" title=\".*?\"><img")

URL = "https://de.wikipedia.org/wiki/Liste_der_Nationalflaggen"



wiki_html = requests.get(URL)

flag_links = REGEX_URL.findall(wiki_html.text)
countries_mal = REGEX_COUNTRY.findall(wiki_html.text)
countries = [country[13:-5] for country in countries_mal]

response = requests.get(f'https://{flag_links[0]}')




def  get_image_to_flag(country, flags_dictionary):
    """
    function that gets a country string and a flag dictionary with 
    keys as country strings and values as imagees
    """
    if country in flags_dictionary.keys():
        return flags_dictionary[country]
    else:
        print("Sorry country not from list or failed to fetch from Wikipedia api.")
if response.status_code == 200:
    # reading png image file 
    im = Image.open(BytesIO(response.content))
     # show image 
else:
    print('Failed to download file')


