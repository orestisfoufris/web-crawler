import unittest

import requests
from mock import MagicMock

from ResponseParser import ResponseParser
from tests.test_data import HOME_PAGE_TEXT, URLS


class ResponseParserTest(unittest.TestCase):

    def setUp(self):
        self.link_parser = ResponseParser()

    def test_find_links_for_domain(self):
        mock_response = MagicMock(requests.Response())
        mock_response.text = HOME_PAGE_TEXT
        mock_response.url = URLS['HOME_PAGE_TEXT']

        actual_pages = self.link_parser.parse_response_for_links(URLS['HOME_PAGE_TEXT'], mock_response, ['a'], {})
        expected_pages = []
        expected_pages.extend(['http://test-page.com/buy', 'http://test-page.com/shopping',
                               'http://test-page.com/contact.html', 'http://test-page.com/books.html',
                               'http://test-page.com/music.html'])

        self.assertEqual(sorted(actual_pages), sorted(expected_pages))

    def test_find_assets_for_domain(self):
        mock_response = MagicMock(requests.Response())
        mock_response.text = HOME_PAGE_TEXT
        mock_response.url = URLS['HOME_PAGE_TEXT']

        actual_assets = {}
        actual_pages = self.link_parser.parse_response_for_links(URLS['HOME_PAGE_TEXT'], mock_response,
                                                                 ['a', 'img', 'rel', 'script'], actual_assets)
        expected_pages = []
        expected_pages.extend(['http://test-page.com/buy', 'http://test-page.com/shopping',
                               'http://test-page.com/contact.html', 'http://test-page.com/books.html',
                               'http://test-page.com/music.html'])

        expected_assets = {'http://test-page.com': {'http://test-page.com/books.html',
                                                           'http://test-page.com/buy',
                                                           'http://test-page.com/music.html/',
                                                           'http://test-page.com/contact.html',
                                                           'http://test-page.com/assets/js/modernizr-2.6.2-min.js',
                                                           'http://test-page.com/buy/',
                                                           'http://test-page.com/shopping'}}

        self.assertEqual(sorted(actual_pages), sorted(expected_pages))
        self.assertEqual(actual_assets, expected_assets)

if __name__ == '__main__':
    unittest.main()
