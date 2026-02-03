import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Same 
from selenium.webdriver.support import expected_conditions as EC # Add from https://stackoverflow.com/questions/62625487/nameerror-name-webdriverwait-is-not-defined
from bs4 import BeautifulSoup


def getsoup(url):

    driver = webdriver.Firefox()
    try: # Ici on try pour etre sur de bien fermer le navigateur a la fin et pas en ouvrir a l'infini
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #On wait pour laisser le temps a la page de se charger

        return soup

    finally:
        driver.quit() # Et ici on ferme


def prix(soup):
    temp = soup.find('div', class_="ProductPrice_below-price-bloc__C0aol")
    return temp.span.string
    


# Tests
print(f"Prix : {prix(getsoup("https://www.millesima.fr/champagne-drappier-carte-d-or-0000.html"))}") # OK