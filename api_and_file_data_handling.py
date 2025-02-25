import requests
import re
from PIL import Image
from io import BytesIO


REGEX_URL = re.compile(
                    r'upload\.wikimedia\.org'
                   + r'/wikipedia/commons/thumb/[\w\d]/[\w\d][\w\d]/F\w*\.'
                   + r'svg/240px-F\w*\.svg\.png'
                   )
REGEX_COUNTRY = re.compile(r"tion\" title=\".*?\"><img")
URL = "https://de.wikipedia.org/wiki/Liste_der_Nationalflaggen"
ENURL = 'https://en.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states'


def get_countries(request_URL,regex_cunt):
    """
    funktion which gets all country codes with help from regular expressions from the 
    wikipedia link also providing the flags
    it returns a collection of strings with all country names
    """
    wiki_html = requests.get(request_URL)
    countries_mal = regex_cunt.findall(wiki_html.text)
    return [country[13:-6] for country in countries_mal]


def get_flag_links(request_URL):
    """
    funktion to find all flag_images with help of regular expressions
    from a Wikipedia html skript.
    It requires a URL as request class and returns the URLs of the flag
    images
    """
    wiki_html = requests.get(request_URL)
    return REGEX_URL.findall(wiki_html.text)

flags = get_flag_links(URL)
for index in range(40):
    print(flags[index])

def get_flags_image_dictionary(flag_urls, countries_lst_de, countries_lst_en):
    """
    function to create a dictionary from flag_urls and 
    countries_lst with countries as keys and flag images as vlaues
    """
    flags_image_dict = dict()
    for index in range(len(countries_lst_en)):
        for flag in flag_urls:
            if countries_lst_en[index] in flag:
                response = requests.get(f'https://{flag}')
                if response.status_code == 200:
                    # reading png image file 
                    flags_image_dict[countries_lst_de[index]] = Image.open(BytesIO(response.content))
                    break
                else:
                    print(f"Bad network connection or link:\n {f'https://{flag}'} corrupted")
                    break
        if countries_lst_de[index] not in flags_image_dict.keys():
            print(f"Country String: {countries_lst_de[index]} corrupted or flag link missing!")
    return flags_image_dict


def  get_image_to_flag(country, flags_dictionary):
    """
    function that gets a country string and a flag dictionary with 
    keys as country strings and values as imagees
    """
    if country in flags_dictionary.keys():
        return flags_dictionary[country]
    else:
        print("Sorry country not from list or failed to fetch from Wikipedia api.")



# get_image_to_flag(get_countries(URL)[3],get_flags_image_dictionary(get_flag_links(URL),get_countries(URL),get_countries(ENURL))).show()