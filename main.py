import csv
from itertools import zip_longest

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from utils import is_url_valid, make_valid_url


options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

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


# df = pd.DataFrame(
#     {
#         "Property Type": property_types,
#         "Price": prices_text,
#         "Location": locations_text,
#         "State": property_states_text,
#         "Descriptions": property_descriptions_text,
#         "Link": property_links_text,
#     }
# )
# df.to_csv("houses.csv", index=False, encoding="utf-8")


#######################################################################################

main_url = "https://casa.sapo.pt/"
pages_contents = []
# start_time = datetime.datetime.now()
for page in range(1, 3, 1):
    page_url = f"https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn={str(page)}"

    with webdriver.Chrome(
        service=ChromeService(executable_path=ChromeDriverManager().install()),
        options=options,
    ) as wd:
        wd.get(page_url)
        content = wd.page_source
        soup = BeautifulSoup(content, "html.parser")
        pages_contents.append(soup)


# def crawl(main_url, num_pages):

#     pages_content = []

#     for page in range(1, 3, 1):
#         page_url = f"https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn={str(page)}"

#         with webdriver.Chrome(
#             service=ChromeService(executable_path=ChromeDriverManager().install()),
#             options=options,
#         ) as wd:
#             wd.get(page_url)
#             content = wd.page_source
#             soup = BeautifulSoup(content, "html.parser")
#             pages_contents.append(soup)


# ola2 = soup.find_all("div", class_="property-info-content")


# property features lists
prices = []
locations = []
property_states = []
property_descriptions = []
property_types = []
property_links = []


for page_content in pages_contents:

    # find the div that contains all the listings
    pc = page_content.find_all("div", class_="property-info-content")

    # find divs for each property item
    prices_text = []
    locations_text = []
    property_states_text = []
    property_descriptions_text = []
    property_types_text = []
    property_links_text = []

    for div in pc:

        # Price
        price_text = div.find("div", class_="property-price-value").text
        prices_text.append(price_text)

        # Location
        location_text = div.find("div", class_="property-location").text
        locations_text.append(location_text)

        # Property State
        property_state_text = div.find("div", class_="property-features-text").text
        property_states_text.append(property_state_text)

        # Property Description
        property_description_text = div.find("div", class_="property-description").text
        property_descriptions_text.append(property_description_text)

        # Property Type
        property_type_text = div.find("div", class_="property-type").text
        property_types_text.append(property_type_text)

        # Property Link
        property_link_text = div.find("a", href=True).get("href")

        if not is_url_valid(property_link_text):
            # not a valid link
            valid_property_link_text = make_valid_url(main_url, property_link_text)
            property_links_text.append(valid_property_link_text)
        else:
            property_links_text.append(property_link_text)

    # add results to list
    prices.extend(prices_text)
    locations.extend(locations_text)
    property_states.extend(property_states_text)
    property_descriptions.extend(property_descriptions_text)
    property_types.extend(property_types_text)
    property_links.extend(property_links_text)


# write results to csv file
csv_headers = ["Property Type", "Price", "Location", "State", "Description", "Link"]

csv_data = [property_types, prices, locations, property_states, property_descriptions, property_links]

export_data = zip_longest(*csv_data, fillvalue="")

with open("houses.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(csv_headers)

    # write the data
    writer.writerows(export_data)


# df = pd.DataFrame(
#     {
#         "Property Type": property_types,
#         "Price": prices,
#         "Location": locations,
#         "State": property_states,
#         "Description": property_descriptions,
#         "Link": property_links,
#     }
# )
# df.to_csv("houses.csv", index=False, encoding="utf-8")


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
