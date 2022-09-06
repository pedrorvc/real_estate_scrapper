import csv
from itertools import zip_longest

from utils import is_url_valid, make_valid_url

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import os
import argparse


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


def main(
    main_url, purpose, type_of_property, location, number_of_rooms, min_price, max_price, pages, output_directory, cpu
):

    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    pass


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "-w",
        "--website",
        type=str,
        required=True,
        choices=[
            "sapo",
        ],
        nargs="+",
        default="sapo",
        dest="websites",
        help="Choose websites to scrape.",
    )

    parser.add_argument(
        "-p",
        "--purpose",
        type=str,
        required=True,
        choices=[
            "buy",
            "rent",
        ],
        dest="purpose",
        help="Purpose of the search.",
    )

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        required=True,
        choices=[
            "apartment",
            "house",
            "land",
            "shop",
            "building",
        ],
        dest="type_of_property",
        help="Type of property to search for.",
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        required=True,
        dest="location",
        help="Location of the property.",
    )

    parser.add_argument(
        "-r",
        "--rooms",
        type=int,
        required=False,
        dest="number_of_rooms",
        help="Number of rooms of the property.",
    )

    parser.add_argument(
        "--min-price",
        type=int,
        required=False,
        dest="min_price",
        help="Minimum price of the property.",
    )

    parser.add_argument(
        "--max-price",
        type=int,
        required=False,
        dest="max_price",
        help="Maximum price of the property.",
    )

    parser.add_argument(
        "--pages",
        type=int,
        required=False,
        default=1,
        dest="pages",
        help="Number of pages to crawl.",
    )

    parser.add_argument(
        "-o",
        "--output-directory",
        type=str,
        required=True,
        dest="output_directory",
        help="Path to the directory to which the results will be stored.",
    )

    parser.add_argument(
        "--cpu", type=int, required=False, default=2, dest="cpu", help="Number of cpu for multiprocessing."
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_arguments()
    main(**vars(args))
