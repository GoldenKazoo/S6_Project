import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Same 
from selenium.webdriver.support import expected_conditions as EC # Add from https://stackoverflow.com/questions/62625487/nameerror-name-webdriverwait-is-not-defined
from bs4 import BeautifulSoup

# Question 1 : recup la soup de la page
def getsoup(url):

    driver = webdriver.Firefox()
    try: # Ici on try pour etre sur de bien fermer le navigateur a la fin et pas en ouvrir a l'infini
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #On wait pour laisser le temps a la page de se charger

        return soup

    finally:
        driver.quit() # Et ici on ferme

# Question 2 : recup prix a partir de soup de la page
def prix(soup):
    temp = soup.find('div', class_="ProductPrice_below-price-bloc__C0aol")
    if temp is None:
        return None
    price = temp.span.string
    price = price.replace(',','.')
    return float(price[:-2])
    
# Question 3
# TODO
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
# TODO

# Question 6
def informations(soup):
    return str(appellation(soup)) + "," + str(parker(soup)) + "," + str(robinson(soup)) + "," + str(suckling(soup)) + "," + str(prix(soup))



# Tests
print(f"Prix : {prix(getsoup("https://www.millesima.fr/chateau-citran-2018.html"))}") # OK
print(f"Rating parker : {parker(getsoup("https://www.millesima.fr/champagne-drappier-carte-d-or-0000.html"))}") 
print(f"Rating parker : {parker(getsoup("https://www.millesima.fr/chateau-lafite-rothschild-2000.html"))}")
#print(f"Rating parker : {parker(getsoup("https://www.millesima.fr/chateau-peyrabon-2019.html"))}")

#print(note("90-93+/100")) Existe avec - et + ???
print(note("17/20"))
print(note("1/20"))
print(note("1/100"))
print(note("90+/100"))
print(note("95-100/100"))
print(note("90-93/100"))

print(appellation(getsoup("https://www.millesima.fr/chateau-gloria-2016.html")))

#print(informations(getsoup("https://www.millesima.fr/chateau-citran-2018.html")))