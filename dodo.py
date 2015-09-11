# -*- coding: utf-8 -*-
"""`dodo` filr for `doit`_ tasks.

.. _doit: http://pydoit.org/

"""
import os.path

# Constants  ----------------------------------------------------------------

HOME = os.path.abspath(os.path.dirname(__file__))
"""Project's home absolute path (`str`)."""

PYLINT_RC_RELPATH = '.pylintrc'
"""Relative path to PyLint configuration file (`str`)."""

SCRAPY_SPIDER = 'github'
"""Scrapy main spider name (`str`)."""


DOIT_CONFIG = {
    'continue': True,
    }
"""`doit` configuration (`dict`)."""


# Tasks  --------------------------------------------------------------------

def task_pep8():
    """Lint some Python module with `pep8`.
    """
    return {
        'actions': ['pep8 %(path)s'],
        'params': [
            {'name': 'path',
             'short': 'p',
             'long': 'path',
             'type': str,
             'default': '',
             'help': 'Python module path to lint with `pep8`',
             }],
        }


def task_pyflakes():
    """Lint some Python module with `pyflakes`.
    """
    return {
        'actions': ['pyflakes %(path)s'],
        'params': [
            {'name': 'path',
             'short': 'p',
             'long': 'path',
             'type': str,
             'default': '',
             'help': 'Python module path to lint with `pyflakes`',
             }],
        }


def task_pylint():
    """Lint some Python module with `pylint`.
    """
    return {
        'actions': ['pylint --rcfile={0} %(path)s'.format(PYLINT_RC_RELPATH)],
        'params': [
            {'name': 'path',
             'short': 'p',
             'long': 'path',
             'type': str,
             'default': '',
             'help': 'Python module path to lint with `pylint`',
             }],
        }


def task_lint():
    """Lint some Python module with all linters.
    """
    return {
        'actions': [
            'pep8 %(path)s',
            'pyflakes %(path)s',
            'pylint --rcfile={0} %(path)s'.format(PYLINT_RC_RELPATH),
            ],
        'params': [
            {'name': 'path',
             'short': 'p',
             'long': 'path',
             'type': str,
             'default': '',
             'help': 'Python module path to lint',
             }],
        }


def task_scrapy():
    """Crawl `Dyabola` with `Scrapy`.
    """
    return {
        'actions': ['scrapy crawl {0}'.format(SCRAPY_SPIDER)],
        'verbosity': 2,
        }
