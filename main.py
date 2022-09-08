import os
import argparse

import utils


def main(
    website, purpose, type_of_property, location, number_of_rooms, min_price, max_price, pages, output_directory, cpu
):

    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    search_params = {
        "purpose": purpose,
        "type_of_property": type_of_property,
        "location": location,
        "number_of_rooms": number_of_rooms,
        "min_price": min_price,
        "max_price": max_price,
    }

    # print(search_params)

    # print(website)

    search_params = {
        "purpose": "buy",
        "type_of_property": "apartment",
        "location": "barreiro",
        "number_of_rooms": 2,
        "min_price": None,
        "max_price": None,
    }

    website = "sapo"

    pages = 2

    output_directory = "/home/pcerqueira/REPOS"

    scrape_results = utils.scrape(website, search_params, pages)

    utils.write_results_to_file(website, scrape_results, output_directory)

    print("DONE!")


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
        default="sapo",
        dest="website",
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
            "apartments",
            "houses",
            "land",
            "shops",
            "buildings",
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
