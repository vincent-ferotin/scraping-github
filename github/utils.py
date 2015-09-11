# -*- coding: utf-8 -*-
"""Scrapy utilities for `github` project.
"""
from __future__ import unicode_literals

from scrapy.linkextractors import LinkExtractor


def extract_links(response, xpaths, tag=None, attr=None):
    """Extract links on a page matching given XPaths.

    :param response:    Scrapy response whose body contains links to extract
    :type response:     :class:`scrapy.http.Response`
    :param xpaths:      unique or iterable of XPath(s) matching links
                        to extract
    :type xpaths:       `unicode` or `iterable` of `unicode`
    :param tag:         tag name from which extract links
    :type tag:          `unicode`
    :param attr:        attribute name in :data:`tag` tag from which extract
                        links
    :type attr:         `unicode`
    :yield:             extracted links (canonicalized URLs), directly usable
                        as :data:`scrapy.http.Request.url` parameters
    :rtype:             `generator` orf `unicode`

    """
    # Construct LinkExtractor parameters
    extractor_attrs = {
        'restrict_xpaths': xpaths,
        'canonicalize': True,
        }
    if tag:
        extractor_attrs['tags'] = (tag,)
    if attr:
        extractor_attrs['attrs'] = (attr,)

    # Extract links
    link_extractor = \
        LinkExtractor(**extractor_attrs)
    links = link_extractor.extract_links(response)

    # Generate links
    for link in links:
        yield link.url
