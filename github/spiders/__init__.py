# -*- coding: utf-8 -*-
"""Scrapy spiders for `github` project.
"""
from __future__ import unicode_literals

from copy import copy
from collections import (
    OrderedDict,
    namedtuple,
    )

from scrapy import Spider
from scrapy.http import FormRequest


# Storage utilities  ---------------------------------------------------------

Project = namedtuple('Project', (
    # Name of the project (`unicode`)
    'name',
    # Short URL of the project, relative to GitHub's homepage (`unicode`)
    'short_url',
    # Directories to crawl in the project's structure, mapped to
    # filenames to crawl in project's structure
    # (`OrderedDict` of (`unicode`: `unicode`))
    'dirs',
    ))
"""Storage for project's informations (:class:`collections.namedtuple`)."""


class CrawledInfos(object):
    """Storage for crawled informations.
    """
    def __init__(self, project_name=None, current_dir=None, filename=None):
        """Instance initialization.

        :param project_name:    name of the project currently crawled
        :type project_name:     `unicode`
        :param current_dir:     current crawled directory in project's structure
        :type current_dir:      `unicode`
        :param filename:        current crawled file's name in project's
                                structure

        """
        self.project_name = project_name
        self.current_dir = current_dir
        self.filename = filename

    def clone_and_update(self, **kwargs):
        """Clone current instance and update clone's attributes.

        :param kwargs:      attributes and their values to update in new
                            cloned instance
        :type kwargs:       `dict` of (`unicode`: object)
        :return:            new clone with attributes updated with
                            :data:`kwargs`
        :rtype:             :class:`CrawledInfos`

        """
        clone = copy(self)
        for attr_name, attr_value in kwargs.iteritems():
            setattr(clone, attr_name, attr_value)

        return clone


# Tree to crawl  --------------------------------------------------------------

PROJECTS = OrderedDict((
    ('Scrapy',
     Project('Scrapy', '/scrapy/scrapy', OrderedDict((
             ('docs', (
                'README',
                'conf.py',
                'faq.rst',
                )),
             ('scrapy', (
                'VERSION',
                'spider.py',
                )),
             ('extras', (
                'scrapy.1',
                'scrapy_zsh_completion',
                )),
             )))),
    ('scrapyd',
     Project('scrapyd', '/scrapy/scrapyd', OrderedDict((
             ('docs', (
                'conf.py',
                'index.rst',
                'install.rst',
                )),
             ('scrapyd', (
                'VERSION',
                'app.py',
                'utils.py',
                )),
             ('extras', (
                'test-scrapyd.sh',
                )),
             )))),
    ('scrapylib',
     Project('scrapylib', '/scrapinghub/scrapylib', OrderedDict((
             ('scrapylib', (
                'redisqueue.py',
                'links.py',
                )),
             ('tests', (
                'test_links.py',
                'test_magicfields.py',
                )),
             )))),
    ))
"""All projects and their informations to crawl
(`dict` of (`unicode`: :class:`Project`))."""


# Spiders  -------------------------------------------------------------------

class GitHubSpider(Spider):
    """`GitHub` spider used to demonstrate Scrapy default tree walking.
    """
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/']

    def parse(self, response):
        """Parse `GitHub`'s homepage.
        """
        search_form_xpath = '//form[@class="js-site-search-form"]'
        yield FormRequest.from_response(response,
                                        callback=self.parse_search_results,
                                        formxpath=search_form_xpath,
                                        formdata={'q': 'scrapy'})

    def parse_search_results(self, response):
        """Parse `GitHub`'s search results.
        """
        repo_urls = response.xpath(('//ul[@class="repo-list js-repo-list"]'
                                     '/li/h3/a/@href')).extract()
        # FIXME: debugging only
        self.logger.debug('REPOS URLs: {0}'.format(', '.join(repo_urls)))
        #######################
