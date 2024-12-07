import base64
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

filmStocks_StuckInFilm = [
    FilmStock("Velvia 50 - 5 Pack - 120", "https://stuckinfilm.co.uk/products/fujifilm-velvia-50-120-film-5-pack"),
    FilmStock("Velvia 100 - 5 Pack - 120", "https://stuckinfilm.co.uk/products/fujifilm-velvia-100-120-film-5-pack"),
    FilmStock("Velvia 100F - 5 Pack - 120", "https://stuckinfilm.co.uk/products/fujifilm-provia-100f-120-film-5-pack"),
]

filmStocks_AnalogWonderland = [
    FilmStock("Velvia 50 - Single Roll - 120", "https://analoguewonderland.co.uk/products/fuji-velvia-film-120-colour-iso-50-5-pack?variant=32208703094844"),
    FilmStock("Velvia 50 - 5 Pack - 120", "https://analoguewonderland.co.uk/products/fuji-velvia-film-120-colour-iso-50-5-pack?variant=32208703062076"),
    FilmStock("Velvia 100 - Single Roll - 120","https://analoguewonderland.co.uk/products/fuji-velvia-film-120-colour-iso-100-5-pack?variant=32208694902844"),
    FilmStock("Velvia 100 - 5 Pack - 120","https://analoguewonderland.co.uk/products/fuji-velvia-film-120-colour-iso-100-5-pack?variant=32208694870076"),
    FilmStock("Velvia 100F - Single Roll - 120","https://analoguewonderland.co.uk/products/fuji-provia-100f-film-120-colour-iso-100-5-pack?variant=32334275084348"),
    FilmStock("Velvia 100F - 5 Pack - 120","https://analoguewonderland.co.uk/products/fuji-provia-100f-film-120-colour-iso-100-5-pack?variant=32334275051580"),
]

while True:

    driver = webdriver.Chrome(options=chrome_options)

    for stock in filmStocks_StuckInFilm:
        driver.get(stock.url)

        elem = driver.find_element(By.CLASS_NAME, "price__badge-sold-out")
        if elem.is_displayed() == False:
            message = stock.name + " " + "is in stock at StuckInFilm"
            print(message)
            requests.post(ntfy_url,
                data=message,
                headers={
                    "Title": "Film Restocked!",
                    "Authorization": authHeader
                })

    for stock in filmStocks_AnalogWonderland:
        driver.get(stock.url)

        elem = driver.find_element(By.CLASS_NAME, "product-form__add-button")
        if elem.text == "Add to cart":
            message = stock.name + " " + "is in stock at Analog Wonderland"
            print(message)
            requests.post(ntfy_url,
                data=message,
                headers={
                    "Title": "Film Restocked!",
                    "Authorization": authHeader
                })

    driver.close()

    time.sleep(3600)
