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

import os
import csv
from itertools import zip_longest
from urllib.parse import urlparse, urljoin, urlencode, parse_qs

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


def is_url_valid(url: str):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def make_valid_url(url: str, href: str):
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


def write_results_to_file(website: str, scraped_data: dict, output_directory: str):
    """Write a CSV file with results of scrapping."""

    # write results to csv file
    csv_headers = ["Property Type", "Price", "Location", "State", "Description", "Link"]

    export_data = zip_longest(*scraped_data, fillvalue="")

    output_file_path = os.path.join(output_directory, f"{website}_houses.csv")

    with open(output_file_path, "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(csv_headers)

        # write the data
        writer.writerows(export_data)


def crawl(page_url: str, num_pages: int):
    """Crawl through webpages."""

    pages_content = []

    for page in range(1, num_pages + 1, 1):

        page_url_to_crawl = page_url.format(page)

        with webdriver.Chrome(
            service=ChromeService(executable_path=ChromeDriverManager().install()),
            options=options,
        ) as wd:
            wd.get(page_url_to_crawl)
            content = wd.page_source
            soup = BeautifulSoup(content, "html.parser")
            pages_content.append(soup)

    return pages_content


def create_sapo_page_url(main_url: str, search_params: dict, num_pages: int):
    """Creates the page url for the sapo website."""

    page_url = f"{main_url}{search_params['purpose']}-{search_params['type_of_property']}/"

    # check number of rooms
    if search_params["number_of_rooms"] is not None:
        # add number of rooms and location
        page_url = urljoin(page_url, f"t{search_params['number_of_rooms']}/{search_params['location']}/")

    else:
        # add location
        page_url = urljoin(page_url, f"{search_params['location']}/")

    if search_params["min_price"] is not None:
        # add minimum price
        page_url = urljoin(page_url, f"?lp={search_params['min_price']}")

        if search_params["max_price"] is not None:
            # add maximum price
            page_url = f"{page_url}&{urlencode({'gp': search_params['max_price']})}"

    elif search_params["max_price"] is not None:
        # add maximum price if minimum was not provided
        page_url = urljoin(page_url, f"?gp={search_params['max_price']}")

    if parse_qs(page_url):
        # min_price and/or max_price query params were added
        page_url_pagination = page_url + "&pn={}"

        return page_url_pagination
    else:
        # query params were not added
        page_url_pagination = page_url + "?pn={}"

        return page_url_pagination


def scrape_sapo(main_url: str, search_params: dict, num_pages: int):
    """Scrape sapo webpage."""

    sapo_page_url = create_sapo_page_url(main_url, search_params, num_pages)

    sapo_page_contents = crawl(sapo_page_url, num_pages)

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

    scraped_data = [
        property_types,
        prices,
        locations,
        property_states,
        property_descriptions,
        property_links,
    ]

    return scraped_data


WEBSITES = {"sapo": {"main_url": "https://casa.sapo.pt/en-gb/", "scrape_func": scrape_sapo}}


def scrape(website: str, search_params: dict, pages: int):
    """Scrape portuguese real estate websites."""

    main_url = WEBSITES[website]["main_url"]

    scrape_results = WEBSITES[website]["scrape_func"](main_url, search_params, pages)

    return scrape_results
