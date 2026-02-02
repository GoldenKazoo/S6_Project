import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
