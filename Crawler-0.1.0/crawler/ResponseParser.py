"""
LinkParser is responsible for extracting all the
information we need from each link
"""

from urlparse import urlparse
from bs4 import BeautifulSoup, SoupStrainer


class ResponseParser(object):

    def __init__(self, encode='utf-8'):
        self.encode_string = lambda x: x.encode(encode)
        self._sanitize_url = lambda x: x.strip("/")

    def parse_response_for_links(self, domain, response, tags_to_parse, links_between_pages, parser='html.parser'):

        encoded_resp = self.encode_string(response.text)

        extracted_links = self._extract_links_from_response(encoded_resp, parser, tags_to_parse)
        pages = self._extract_valid_pages(self.encode_string(response.url), extracted_links,
                                          self._sanitize_url(domain), links_between_pages)

        return pages

    @staticmethod
    def _find_adjacent_links(parent_url, page_assets, links_between_pages):
        if parent_url not in links_between_pages:
            links_between_pages[parent_url] = set()
        else:
            adjacent_links = links_between_pages.get(parent_url)
            adjacent_links.add(page_assets)

    @staticmethod
    def _extract_links_from_response(encoded_resp, parser, tags_to_parse):
        """
        :return: a BeautifulSoup object that includes response's text
        based on the tags argument
        """
        soup_strainer = SoupStrainer(tags_to_parse)
        return BeautifulSoup(encoded_resp, parser, parse_only=soup_strainer)

    def _extract_valid_pages(self, parent_url, links, domain, links_between_pages):
        """
        returns a set of pages found and populates
        the assets/links for every page
        """
        pages = set()
        for link in links:
            href = link.get('href')
            rel = link.get('src')

            if href is not None and not href.startswith('../'):
                if self._is_valid_url(urlparse(href)):
                    next_pages = self._find_asset(urlparse(href), domain)
                    if next_pages != '':
                        pages.add(self._sanitize_url(next_pages))
                        self._find_adjacent_links(parent_url, next_pages, links_between_pages)

            if rel is not None and not rel.startswith('../'):
                next_assets = self._find_asset(urlparse(rel), domain)
                if next_assets != '':
                    self._find_adjacent_links(parent_url, self._sanitize_url(next_assets), links_between_pages)

        return pages

    @staticmethod
    def _is_valid_url(parsed_url):
        """
        :return: True if the url is a HTML page
        otherwise false
        """
        path_extension = parsed_url.path.split('/')[-1]
        extension = path_extension.rfind(".")
        if extension != -1:
            return path_extension[extension+1:] == 'html'

        return True

    def _find_asset(self, link, domain):
        """
        This method assembles the link or asset
        and returns it -> String
        """
        if link.scheme != '' and link.netloc == urlparse(domain).netloc :
            return self.encode_string(link.scheme + '://' + link.netloc + link.path)

        if link.fragment == '' and link.scheme == '':
            if link.netloc == domain: # we filter out external pages
                return self.encode_string(link)
            elif link.netloc == '':
                if self.encode_string(link.path).startswith('/'):
                    return domain + self.encode_string(link.path)
                else:
                    return domain + '/' + self.encode_string(link.path)
        return ''
