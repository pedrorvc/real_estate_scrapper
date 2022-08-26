import datetime

from selenium import webdriver

from selenium.webdriver.common.by import By
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
# driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)


# page_url = "https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn=1"

# driver.get(page_url)
# title = driver.find_elements(by=By.CLASS_NAME, value="featured-property-header")

# for i in title:
#     print(i.text)

# content = driver.page_source
# soup = BeautifulSoup(content)


# closing the driver
# driver.close()

# create lists to store results
# prices_text = []
# locations_text = []
# property_states_text = []
# property_descriptions_text = []
# property_links_text = []
# property_types_text = []


# elems = []


# start_time = datetime.datetime.now()
# for page in range(1, 3, 1):
#     page_url = f"https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn={str(page)}"

#     with webdriver.Chrome(
#         service=ChromeService(executable_path=ChromeDriverManager().install()), options=options
#     ) as wd:
#         wd.get(page_url)
#         # content = wd.page_source
#         # soup = BeautifulSoup(content)
#         # elems.append(soup)

#         prices = wd.find_elements(By.XPATH, "//div[@class='property-price-value']")
#         locations = wd.find_elements(By.XPATH, "//div[@class='property-location']")
#         property_states = wd.find_elements(By.XPATH, "//div[@class='property-features-text']")
#         property_descriptions = wd.find_elements(By.XPATH, "//div[@class='property-description']")
#         property_types = wd.find_elements(By.XPATH, "//div[@class='property-type']")

#         prices_text.extend([price.text for price in prices])
#         locations_text.extend([location.text for location in locations])
#         property_states_text.extend([state.text for state in property_states])
#         property_descriptions_text.extend([description.text for description in property_descriptions])
#         property_types_text.extend([p_type.text for p_type in property_types])
#         # property_links_text
#         # property_types_text

# end_time = datetime.datetime.now()
# print(end_time - start_time)


df = pd.DataFrame(
    {
        "Property Type": property_types,
        "Price": prices_text,
        "Location": locations_text,
        "State": property_states_text,
        "Descriptions": property_descriptions_text,
        "Link": property_links_text,
    }
)
df.to_csv("houses.csv", index=False, encoding="utf-8")


#######################################################################################

pages_contents = []
# start_time = datetime.datetime.now()
for page in range(1, 3, 1):
    page_url = f"https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn={str(page)}"

    with webdriver.Chrome(
        service=ChromeService(executable_path=ChromeDriverManager().install()), options=options
    ) as wd:
        wd.get(page_url)
        content = wd.page_source
        soup = BeautifulSoup(content)
        pages_contents.append(soup)

# ola2 = soup.find_all("div", class_="property-info-content")


prices = []


for page_content in pages_contents:

    # find the div that contains the listings
    pc = page_content.find_all("div", class_="property-info-content")

    prices_text = [price.find("div", class_="property-price-value").text for price in pc]

    prices.extend(prices_text)


# prices = []

# for property_info_list in property_info_lists:

#     # scrap results
#     price0 = property_info_list.find("div", class_="property-price-value")

#     prices.extend([p0.text for p0 in price0])

# contn = o.find_all("div", class_="property-info-content")

# # scrap results
# price0 = [co.find("div", class_="property-price-value") for co in contn]

# # price0 = o.find("div", class_="property-price-value")
# # location = o.find("div", class_="property-location")
# # property_state = o.find("div", class_="property-features-text")
# # property_description = o.find("div", class_="property-description")
# # property_type = o.find("div", class_="property-type")
# # property_link = o.find("a", href=True)

# # add results to lists
# prices2.extend([p0.text for p0 in price0])

# # prices2.append(price0.text)
# # locations.append(location.text)
# # property_states.append(property_state.text)
# # property_descriptions.append(property_description.text)
# # property_types.append(property_type.text)
# # property_links.append(property_link["href"])

# end_time = datetime.datetime.now()
# print(end_time - start_time)


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
