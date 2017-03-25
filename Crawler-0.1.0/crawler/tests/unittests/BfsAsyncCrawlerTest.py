import unittest

import requests
from mock import MagicMock

from BfsAsyncCrawler import BfsAsyncCrawler
from RequestsExecutorAsync import RequestsExecutorAsync
from ResponseParser import ResponseParser
from tests.test_data import URLS


class BfsAsyncCrawlerTest(unittest.TestCase):

    def setUp(self):
        self.mock_req_executor = MagicMock(RequestsExecutorAsync())
        self.mock_link_parser = MagicMock(ResponseParser())

        self.bfs_crawler = BfsAsyncCrawler(self.mock_req_executor, self.mock_link_parser)

    def test_perform_crawling(self):
        headers = {'content-type': 'text/html'}

        mock_response = MagicMock(requests.Response())
        mock_response.headers = headers

        self.mock_req_executor.send_requests.return_value = [mock_response]

        self.mock_link_parser.parse_response_for_links.side_effect = [
            ['http://test-page.com/buy', 'http://test-page.com/shopping'],
            ['http://test-page.com/songs'], []
        ]

        actual_sitemap, actual_assets = self.bfs_crawler.crawl(URLS['HOME_PAGE_SIMPLE'], ['a'])

        self.assertEqual(sorted(actual_sitemap), sorted(['http://test-page.com/buy\n',
                                                         'http://test-page.com/shopping\n',
                                                         'http://test-page.com/songs\n',
                                                         'http://test-page.com\n']))
        self.assertTrue(len(actual_assets) == 0)

        mock_req_executor_calls = self.mock_req_executor.mock_calls
        self.assertEqual(len(mock_req_executor_calls), 3)

    def test_perform_crawling_with_circle(self):
        """
        We have created a circle here where /buy returns links
        to /shopping and /shopping link to buy
        """
        headers = {'content-type' : 'text/html'}

        first_mock_response = MagicMock(requests.Response())
        second_mock_response = MagicMock(requests.Response())

        first_mock_response.headers = headers
        second_mock_response.headers = headers

        self.mock_req_executor.send_requests.side_effect = [[first_mock_response], [second_mock_response],
                                                            [first_mock_response], [second_mock_response],
                                                            [first_mock_response]]

        self.mock_link_parser.parse_response_for_links.side_effect = [
            ['http://test-page.com/shopping'],
            ['http://test-page.com/buy'],
            ['http://test-page.com/shopping'],
            ['http://test-page.com/buy'],
            []
        ]

        self.bfs_crawler.crawl(URLS['BUY_PAGE_TEXT'], ['a'])

        mock_req_executor_calls = self.mock_req_executor.mock_calls
        self.assertEqual(len(mock_req_executor_calls), 2)

    def test_perform_crawling_with_limit(self):
        """
        We have created a circle here where /buy returns links
        to /shopping and /shopping link to buy
        """
        headers = {'content-type' : 'text/html'}

        first_mock_response = MagicMock(requests.Response())
        second_mock_response = MagicMock(requests.Response())

        first_mock_response.headers = headers
        second_mock_response.headers = headers

        self.mock_req_executor.send_requests.side_effect = [[first_mock_response], [second_mock_response],
                                                            [first_mock_response], [second_mock_response],
                                                            [first_mock_response]]

        self.mock_link_parser.parse_response_for_links.side_effect = [
            ['http://test-page.com/shopping'],
            ['http://test-page.com/home'],
            ['http://test-page.com/pay'],
            ['http://test-page.com/refund'],
            []
        ]

        self.bfs_crawler.crawl(URLS['BUY_PAGE_TEXT'], ['a'], 2)

        mock_req_executor_calls = self.mock_req_executor.mock_calls

        # starting_url is not included so it should be limit + 1
        self.assertEqual(len(mock_req_executor_calls), 3)

if __name__ == '__main__':
    unittest.main()
