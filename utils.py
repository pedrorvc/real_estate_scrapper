#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 17:43:24 2022

@author: pcerqueira

Purpose
-------

This module contains utility functions
for the main scrapper script.

"""
import csv
from itertools import zip_longest

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# selenium options
options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")


def is_url_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def make_valid_url(url, href):
    """ """
    # join the URL if it's relative (not absolute link)
    href = urljoin(url, href)
    parsed_href = urlparse(href)

    # remove URL GET parameters, URL fragments, etc.
    href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

    if is_url_valid(href):
        return href
    else:
        return "NOT A VALID LINK"


def write_results_to_file(website, data):
    """ """

    # write results to csv file
    csv_headers = ["Property Type", "Price", "Location", "State", "Description", "Link"]

    csv_data = [property_types, prices, locations, property_states, property_descriptions, property_links]

    export_data = zip_longest(*csv_data, fillvalue="")

    with open(f"{website}_houses.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(csv_headers)

        # write the data
        writer.writerows(export_data)


def crawl(main_url, search_params, num_pages):
    """ """

    pages_content = []

    for page in range(1, num_pages + 1, 1):
        page_url = f"https://casa.sapo.pt/comprar-apartamentos/t2/barreiro/?lp=50000&gp=200000&pn={str(page)}"

        with webdriver.Chrome(
            service=ChromeService(executable_path=ChromeDriverManager().install()),
            options=options,
        ) as wd:
            wd.get(page_url)
            content = wd.page_source
            soup = BeautifulSoup(content, "html.parser")
            pages_content.append(soup)

    return pages_content


websites_dict = {"sapo": "https://casa.sapo.pt/"}


def scrape_sapo(main_url, sapo_page_contents):
    """ """

    # property features lists
    prices = []
    locations = []
    property_states = []
    property_descriptions = []
    property_types = []
    property_links = []

    for page_content in sapo_page_contents:

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

    scraped_data = {
        "prices": prices,
        "locations": locations,
        "states": property_states,
        "descriptions": property_descriptions,
        "types": property_types,
        "links": property_links,
    }

    return scraped_data


def scrape(website):
    """ """
    pass
