
from abc import ABCMeta, abstractmethod


class BaseCrawler(object):

    __metaclass__ = ABCMeta

    def __init__(self, requests_executor, link_parser):
        self.requests_orchestrator = requests_executor
        self.link_parser = link_parser
        self.crawl_limit = None
        self.links_between_pages = {}
        self.sitemap = None

    def crawl(self, starting_url, required_tags=None, crawl_limit=None):
        self.links_between_pages = {}

        return self.perform_crawling(starting_url.strip('/'), self.links_between_pages, required_tags, crawl_limit)

    @abstractmethod
    def perform_crawling(self, starting_url, links_between_pages, required_tags, crawl_limit):
        pass
