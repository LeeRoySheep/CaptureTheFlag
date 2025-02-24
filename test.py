import requests
import re
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import Text, filedialog
 
root = tk.Tk()
 
 
def forecast():
    print("My Forecast")
    label['text'] = "My Forecast"
 
 
def models():
    print("Models selected. ")
    label['text'] = "Models selected. "
 
 
canvas = tk.Canvas(root, height=480, width=640, bg='black')
canvas.pack()
 
frame = tk.Frame(root, bg='black')
frame.place(relwidth=0.6, relheight=0.6, relx=0.1, rely=0.1)
label = tk.Label(frame, fg='white', bg='black')
label.pack()
forecast = tk.Button(root, text="Forecasts", padx=2, pady=3,
                     fg='white', bg="red", command=forecast)
forecast.pack()
 
models = tk.Button(root, text="Models", padx=2, pady=3,
                   fg='white', bg="red", command=models)
models.pack()
 
tk.mainloop()


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

if response.status_code == 200:
    # reading png image file 
    im = Image.open(BytesIO(response.content))
     # show image 
    im.show()
    print(f'{countries[0]}File downloaded successfully')
else:
    print('Failed to download file')

