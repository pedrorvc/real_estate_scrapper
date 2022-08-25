from selenium import webdriver

# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import pandas as pd

options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# driver = webdriver.Chrome("/home/pcerqueira/COURSES/SCRAPPER/chromedriver_linux64/chromedriver")
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)


page_url = "https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn=1"

driver.get(page_url)
# title = driver.find_elements(by=By.CLASS_NAME, value="featured-property-header")

# for i in title:
#     print(i.text)

content = driver.page_source
soup = BeautifulSoup(content)


# closing the driver
driver.close()

# create lists to store results
prices = []
locations = []
property_states = []
property_descriptions = []
property_links = []
property_types = []

ola2 = soup.find_all("div", class_="property-info-content")


elems = []

for page in range(1, 3, 1):
    page_url = f"https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn={str(page)}"

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(page_url)
    content = driver.page_source
    driver.close()
    soup = BeautifulSoup(content)
    elems.append(soup)


for o in ola2:

    # scrap results
    price = o.find("div", class_="property-price-value")
    location = o.find("div", class_="property-location")
    property_state = o.find("div", class_="property-features-text")
    property_description = o.find("div", class_="property-description")
    property_type = o.find("div", class_="property-type")
    property_link = o.find("a", href=True)

    # add results to lists
    prices.append(price.text)
    locations.append(location.text)
    property_states.append(property_state.text)
    property_descriptions.append(property_description.text)
    property_types.append(property_type.text)
    property_links.append(property_link["href"])


df = pd.DataFrame(
    {
        "Property Type": property_types,
        "Price": prices,
        "Location": locations,
        "State": property_states,
        "Descriptions": property_descriptions,
        "Link": property_links,
    }
)
df.to_csv("houses.csv", index=False, encoding="utf-8")


# for holding the resultant list
# element_list = []

# for page in range(1, 3, 1):

#     page_url = (
#         "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page="
#         + str(page)
#     )
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver.get(page_url)
#     title = driver.find_elements(by=By.CLASS_NAME, value="title")
#     price = driver.find_elements(by=By.CLASS_NAME, value="price")
#     description = driver.find_elements(by=By.CLASS_NAME, value="description")
#     rating = driver.find_elements(by=By.CLASS_NAME, value="rating")

#     for i in range(len(title)):
#         element_list.append(
#             [title[i].text, price[i].text, description[i].text, rating[i].text]
#         )

# print(element_list)

# closing the driver
# driver.close()
