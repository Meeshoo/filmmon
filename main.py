import base64
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

ntfy_url = "ntftUrlHerePlease"
ntfy_username = "ntfyUsernameHerePlease"
ntfy_password = "ntfyPasswordHerePlease"

credentials = ntfy_username + ":" + ntfy_password

credentialsBytpes = base64.b64encode(credentials.encode('utf-8'))
token = credentialsBytpes.decode('utf-8')

authHeader = "Basic " + token

class FilmStock:
    def __init__(self, name, url):
        self.name = name
        self.url = url

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") 

# filmStocks = [
#     FilmStock("Velvia 50 - 5 Pack - 120", "https://stuckinfilm.co.uk/products/fujifilm-velvia-50-120-film-5-pack"),
#     FilmStock("Velvia 100 - 5 Pack - 120", "https://stuckinfilm.co.uk/products/fujifilm-velvia-100-120-film-5-pack"),
#     FilmStock("Velvia 100F - 5 Pack - 120", "https://stuckinfilm.co.uk/products/fujifilm-provia-100f-120-film-5-pack"),
# ]

filmStocks = [
    FilmStock("Velvia 50 5 Pack in 120", "https://stuckinfilm.co.uk/products/fujifilm-velvia-50-120-film-5-pack"),
    FilmStock("Gold 200 5 Pack in 120", "https://stuckinfilm.co.uk/products/kodak-gold-200-120-film-1-roll")
]

while True:

    driver = webdriver.Chrome(options=chrome_options)

    for stock in filmStocks:
        driver.get(stock.url)

        elem = driver.find_element(By.CLASS_NAME, "price__badge-sold-out")
        if elem.is_displayed() == False:
            message = stock.name + " " + "is in stock"
            print(message)
            requests.post(ntfy_url,
                data=message,
                headers={
                    "Title": "Film is in stock",
                    "Authorization": authHeader
                })

    driver.close()

    time.sleep(3600)
