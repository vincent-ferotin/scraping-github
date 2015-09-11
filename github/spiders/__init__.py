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
from scrapy.http import (
    FormRequest,
    Request,
    )

from github.utils import extract_links


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
        repo_link_xpath = ('//ul[@class="repo-list js-repo-list"]'
                           '/li/h3/a')
        repo_urls = set(response.xpath(('{0}/@href'.format(repo_link_xpath)))\
                                .extract())

        for project in PROJECTS.itervalues():
            if project.short_url not in repo_urls:
                self.logger.error(('NOT FIND {0} in repos. URLs! Skipping '
                                   'project `{1}`...').format(project.short_url,
                                                              project.name))
                continue
            # else:
            crawled_infos = CrawledInfos(project_name=project.name)

            link_xpath = '{0}[@href="{1}"]'.format(repo_link_xpath,
                                                   project.short_url)
            next_url = list(extract_links(response, xpaths=link_xpath))[0]

            yield Request(next_url,
                          callback=self.parse_project,
                          meta={
                            'crawled_infos': crawled_infos,
                            'project': project,
                            })

    def parse_project(self, response):
        """Parse project's homepage on GitHub.

        :meta crawled_infos:    currently crawled informations
        :type crawled_infos:    :class:`CrawledInfos`
        :meta project:          current crawled project
        :type project:          :class:`Project`

        """
        crawled_infos = response.meta['crawled_infos']
        project = response.meta['project']

        item_xpath = '//a[@class="js-directory-link js-navigation-open"]'
        dir_items = set(response.xpath('{0}/text()'.format(item_xpath))\
                                .extract())

        for dirname in project.dirs:
            if dirname not in dir_items:
                self.logger.error(('NOT FIND `{0}` directory in repo. `{1}`! '
                                   'Skipping item...'
                                   '').format(dirname, project.short_url))
                continue

            _crawled_infos = \
                crawled_infos.clone_and_update(current_dir=dirname)

            link_xpath = '{0}[text()="{1}"]'.format(item_xpath, dirname)
            next_url = list(extract_links(response, xpaths=link_xpath))[0]

            yield Request(next_url,
                          callback=self.parse_directory,
                          meta={
                            'crawled_infos': _crawled_infos,
                            'project': project,
                            })

    def parse_directory(self, response):
        """Parse project's given directory.

        :meta crawled_infos:    currently crawled informations
        :type crawled_infos:    :class:`CrawledInfos`
        :meta project:          current crawled project
        :type project:          :class:`Project`

        """
        crawled_infos = response.meta['crawled_infos']
        project = response.meta['project']

        # FIXME: debugging
        self.logger.debug(('NOW ON `{0}` / `{1}`...'
                           '').format(crawled_infos.project_name,
                                      crawled_infos.current_dir))
        ##################
