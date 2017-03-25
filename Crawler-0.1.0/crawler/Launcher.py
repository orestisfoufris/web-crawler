"""
Launcher of the application
"""
import argparse
import re

from ResponseParser import ResponseParser
from RequestsExecutorAsync import RequestsExecutorAsync
from BfsAsyncCrawler import BfsAsyncCrawler


class Launcher(object):

    def __init__(self, starting_url, required_tags=None):
        self.starting_url = starting_url

        requests_executor = RequestsExecutorAsync()
        response_parser = ResponseParser()

        self.crawler = BfsAsyncCrawler(requests_executor, response_parser)
        self.required_tags = required_tags

    def run(self, crawl_limit):
        sitemap, assets = self.crawler.crawl(self.starting_url, self.required_tags, crawl_limit)
        self._print_sitemap(sitemap)
        self._print_assets(assets)

    @staticmethod
    def _print_sitemap(sitemap):
        print 'Sitemap:'
        print ''.join(sitemap)

    @staticmethod
    def _print_assets(assets):
        print 'Assets per page:'
        print ''.join(assets)


if __name__ == '__main__':
    def _is_valid_url(url):
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and regex.search(url)


    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="The url you want to crawl")
    parser.add_argument("--limit", help="The number of pages you want to discover."
                                        "Starting url is excluded", default=None)

    args = parser.parse_args()

    if not(_is_valid_url(args.url)):
        raise Exception(str(args.url) + ' is invalid. Please enter a valid url')

    limit = int(args.limit) if args.limit != None else None

    launcher = Launcher(str(args.url).lower(), ['a', 'img', 'rel', 'script'])
    launcher.run(limit)
