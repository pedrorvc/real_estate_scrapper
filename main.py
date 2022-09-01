import csv
from itertools import zip_longest

from utils import is_url_valid, make_valid_url

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

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
