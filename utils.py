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

from urllib.parse import urlparse, urljoin


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
