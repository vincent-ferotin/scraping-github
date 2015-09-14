Demo of scraping `GitHub`'s page to illustrate "depth-first" order of `Scrapy`
==============================================================================

This repository contains a `Scrapy <http://scrapy.org/>`_ project scraping
first pages of three `GitHub <https://github.com/>`_\ 's projects,
and some figures of its results.
It aims to demonstrate that `Scrapy` so-called `"depth-first" order
<http://doc.scrapy.org/en/1.0/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order>`_
is actually a **breadth-first order**.

`Scrapy` project crawls some :ref:`given and specified web structure <structure>`,
and outputs both requests and responses proceeded orders,
allowing to reconstruct walked graph.

Actually crawling orders for both requests and responses are stored (by hand)
in graphs in ``tree/`` directory (files created with `Inkscape
<http://www.inkscape.org/>`_\ ). They exist for :ref:`two configurations
<configurations>` of `Scrapy`,
default one (files named ``github-tree-*-depth_priority_0``) described
as configuration for "depth-first" order, and alternative configuration
(files named ``github-tree-*-depth_priority_1``) for "breadth-first" order.


.. _structure:

Scraped structure
-----------------

Project scraps three `GitHub`\ 's projects (``scrapy/scrapy``, ``scrapy/scrapyd``,
``scrapinghub/scrapylib``) and in each project scraps 3 directories,
then in each of these directories one, two or three files.

Complete crawled structure follows,
and is defined in project as :data:`github.spiders.PROJECTS`\ ::

    github.com
     \_ scrapy/scrapy
         \_ docs/
             \_ README,
             \_ conf.py
             \_ faq.rst
         \_ scrapy/
             \_ VERSION
             \_ spider.py
         \_ extras
             \_ scrapy.1
             \_ scrapy_zsh_completion
     \_ scrapy/scrapyd
         \_ docs/
             \_ conf.py
             \_ index.rst
             \_ install.rst
         \_ scrapyd/
             \_ VERSION
             \_ app.py
             \_ utils.py
         \_ extras
             \_ test-scrapyd.sh
     \_ scrapinghub/scrapylib
         \_ scrapylib/
             \_ redisqueue.py
             \_ links.py
         \_ tests/
             \_ test_links.py
             \_ test_magicfields.py

For each parent node, its direct children order is specified above as top-bottom,
e.g. crawler at ``scrapy/scrapy`` project and ``docs/`` directory will request
``README`` first, then ``conf.py`` and finally ``faq.rst``.


.. _configurations:

Configurations
--------------

Configuration of project is done through ``github/settings.py``.
Default configuration, as documented by Scrapy here:
http://doc.scrapy.org/en/1.0/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order ,
is for "depth-first" order.

To switch to "breadth-first" order, uncomment last lines as such::

    DEPTH_PRIORITY = 1
    SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
    SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

