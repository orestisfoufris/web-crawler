I. Introduction
---------------

This project is about a simple web crawler. Given a starting url the program will discover all links on that specific domain
following the constraints below:

1. Only follow same domain pages
2. Only explore HTML files

Additionally to the sitemap it will output a list of links and assets for each visited page.

II. Design
----------

Internally the crawler will do a Breath-First-Search traversal with the starting url as the root of the tree.
To achieve better performance we have parallelized the IO work we need to do for every level of the tree. He have achieved
that by using a sentinel to mark each level.

When we gather all the links for each level we asynchronously open the urls using the grequests module. Then we parse
each response with the ResponseParser object and extract adjacent links and assets.

III. How to run the Crawler
---------------------------

Run the following command on your terminal from project's root directory to install the project for development:

```
orestis:Crawler orestis$ python setup.py develop
```

The entry point of the program is the Launcher.py inside the crawler directory which you can execute from the command line with:

```
orestis:Crawler/crawler orestis$ python Launcher.py --url YOUR_URL_HERE
```

You can get more information by executing:

```
orestis:Crawler/crawler orestis$ python Launcher.py --help
```

which outputs the command line arguments you can use:

```
usage: Launcher.py [-h] [--url URL] [--limit LIMIT]

optional arguments:
  -h, --help     show this help message and exit
  --url URL      The url you want to crawl
  --limit LIMIT  The number of pages you want to discover.Starting url is
                 excluded
```

IV. Further actions
-------------------

1. Increase test coverage
2. Use a logger to log messages and exceptions instead of printing to sdout



