import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Same 
from selenium.webdriver.support import expected_conditions as EC # Add from https://stackoverflow.com/questions/62625487/nameerror-name-webdriverwait-is-not-defined
from bs4 import BeautifulSoup
import csv
import time
from selenium.webdriver.firefox.options import Options

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option) #Ouverture page unique
URL = "https://www.millesima.fr/"
# option = Options()
# option.headless = True
# Question 1 : recup la soup de la page

def getsoup(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #On wait pour laisser le temps a la page de se charger
    return soup



# Question 2 : recup prix a partir de soup de la page
def prix(soup):
    temp = soup.find('div', class_="ProductPrice_below-price-bloc__C0aol")
    if temp is None:
        return None
    price = temp.span.string
    price = price.replace(',','.')
    return float(price[:-2])
    
# Question 3

def appellation(soup):
    categorie = soup.find_all("tr")[2]
    appellation = categorie.find_all("td")[1]
    return appellation.get_text(strip=True)

    
# Question 4
def parker(soup):
    notations = soup.find_all('span', class_="WineCriticSlide_name__qih2Y")
    for i in range(len(notations)):
        #print(notations[i].string)
        if(notations[i].string == "Parker"):
            print("[+] Parker found !")
            parker_notation = soup.find('span', class_="WineCriticSlide_rating__jtxAA").string
            return note(parker_notation)
        else:
            return None


def note(str):
    tmp = ""
    index = str.index("/")
    for i in range(index):
        if (str[i] == '+'):
            return int(tmp)
        if (str[i] == '-'):
            tmp2 = str[i+1:index]
            print(f"Split : {tmp2}")
            return (int(tmp) + int(tmp2))/2
        tmp += str[i]

    return int(tmp)


# Question 5

def find_critic(soup, str):
    notations = soup.find_all('span', class_="WineCriticSlide_name__qih2Y")
    for i in range(len(notations)):
        # print(notations[i].string)
        if(notations[i].string == str):
            print(str)
            notations = soup.find('span', class_="WineCriticSlide_rating__jtxAA").string
            return note(notations)
    return None

def robinson(soup):
    return (find_critic(soup, "J. Robinson"))


def suckling(soup):
    return(find_critic(soup, "J. Suckling"))

def note(str):
    tmp = ""
    index = str.index("/")
    for i in range(index):
        if (str[i] == '+'):
            return int(tmp)
        if (str[i] == '-'):
            tmp2 = str[i+1:index]
            print(f"Split : {tmp2}")
            return (int(tmp) + int(tmp2))/2
        tmp += str[i]

    return int(tmp)

# Question 6
def informations(soup):
    return str(appellation(soup)) + "," + str(parker(soup)) + "," + str(robinson(soup)) + "," + str(suckling(soup)) + "," + str(prix(soup))

# Question 7
def fill_csv():
    with open ("wine.csv", "w", newline="\n", encoding="utf-8") as file: # https://stackoverflow.com/questions/61861172/what-does-the-argument-newline-do-in-the-open-function et utf-8 pour eviter d'avoir des char bizarre a la p;lace des accents
       writer = csv.writer(file)
       writer.writerow(["Appelation", "Rober", "Robinson", "Suckling", "Prix"])
       page = 1
       while True:
        url = f"{URL}/bordeaux.html?page={page}"
        soup = getsoup(url)
        wine_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_link = URL + href
            if href.endswith(".html") and "chateau" in href and full_link not in wine_links and any(c.isdigit() for c in href):
                wine_links.append(full_link)
        if not wine_links:
            print("WHAT")
            break
        for link in wine_links:
            try:
                wine_soup = getsoup(link)
                line = informations(wine_soup)
                writer.writerow(line.split(","))
                print("C'est good =) lien obtenu:", link)
                time.sleep(1)
            except Exception as e:
                print("Erreur lors de l'obtention du lien :", link)
        page = page + 1
    driver.quit()


# Tests
# print(informations(getsoup("https://www.millesima.fr/chateau-gloria-2016.html")))
# print(f"Prix : {prix(getsoup("https://www.millesima.fr/chateau-citran-2018.html"))}") # OK
# print(f"Rating parker : {parker(getsoup("https://www.millesima.fr/champagne-drappier-carte-d-or-0000.html"))}") 
# print(f"Rating parker : {parker(getsoup("https://www.millesima.fr/chateau-lafite-rothschild-2000.html"))}")
# print(f"Robinson rate : {robinson(getsoup("https://www.millesima.fr/chateau-lafite-rothschild-2000.html"))}")
# print(f"Suckling rate : {suckling(getsoup("https://www.millesima.fr/chateau-lafite-rothschild-2000.html"))}")
#print(f"Rating parker : {parker(getsoup("https://www.millesima.fr/chateau-peyrabon-2019.html"))}")
fill_csv()
#print(note("90-93+/100")) Existe avec - et + ???
# print(note("17/20"))
# print(note("1/20"))
# print(note("1/100"))
# print(note("90+/100"))
# print(note("95-100/100"))
# print(note("90-93/100"))

# print(appellation(getsoup("https://www.millesima.fr/chateau-gloria-2016.html")))

# print(informations(getsoup("https://www.millesima.fr/chateau-citran-2018.html")))