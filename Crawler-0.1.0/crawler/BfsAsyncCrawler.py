"""
A Crawler that discovers links using Breath-First-Search
"""
import time
from collections import deque

from BaseCrawler import BaseCrawler

SENTINEL = 'SENTINEL'


class BfsAsyncCrawler(BaseCrawler):

    def __init__(self, requests_executor, response_parser):
        super(BfsAsyncCrawler, self).__init__(requests_executor, response_parser)
        self.crawl_limit = None

    def perform_crawling(self, starting_url, links_between_pages, required_tags, crawl_limit):
        self.crawl_limit = crawl_limit
        self.sitemap = self._async_bfs_crawling(starting_url, links_between_pages, required_tags)

        return self.sitemap, self._get_links_between_pages()

    def _async_bfs_crawling(self, starting_url, links_between_pages, required_tags=None):
        """
        Perform an asynchronous breath-first-search crawl
        Use a SENTINEL to mark levels on the graph
        :return: a list with all the links discovered
        """
        if required_tags is None:
            required_tags = ['a', 'img', 'rel', 'script']

        queue = deque()
        visited_links = set()
        result = [starting_url + '\n']

        start = time.time()
        queue.append(starting_url)
        queue.append(SENTINEL)

        while not len(queue) == 0:
            links = []
            # drain each level of the tree so we batch requests
            while not len(queue) == 0:
                next_item = queue.popleft()
                if next_item != SENTINEL:
                    links.append(next_item)
                else:
                    break

            responses = self._send_requests(links)

            # mark visited to avoid infinite loops
            for link in links:
                visited_links.add(link)

            adjacent_links = self._find_adjacent_links(responses, starting_url, required_tags, links_between_pages)
            unique_links = self._populate_queue(adjacent_links, visited_links, queue)

            result.extend([link + '\n' for link in unique_links])

            del links[:]

        # TODO: log instead of printing
        print 'Crawling took ' + str(time.time() - start) + ' seconds'
        print 'Total number of url were visited were ' + str(len(result)) + '\n'

        return result

    def _send_requests(self, links):
        result = self.requests_orchestrator.send_requests(links)
        return result

    def _find_adjacent_links(self, responses, domain, required_tags, links_between_pages):
        result = []

        for response in responses:
            cont_type = response.headers.get('content-type')
            if cont_type is not None and cont_type.startswith('text/html'):
                pages = self._find_pages_assets(domain, links_between_pages, required_tags, response)
                result.extend(pages)

        return result

    def _find_pages_assets(self, domain, links_between_pages, required_tags, response):
        return self.link_parser.parse_response_for_links(domain, response, required_tags, links_between_pages)

    def _get_links_between_pages(self):
        """
        :return: an array containing links and assets for each page
        """
        result = []
        for source, value in self.links_between_pages.iteritems():
            result.append(source + '\n')
            for asset in value:
                result.append('\t' + asset + '\n')

        return result

    def _crawl_limit_checker(self):
        if self.crawl_limit is None:
            return False

        self.crawl_limit -= 1
        return self.crawl_limit < 0

    def _populate_queue(self, links_found, visited_links, bfs_queue):
        local_seen = set()
        unique_links = []

        for link in links_found:
            if link not in visited_links and link not in local_seen:
                if self._crawl_limit_checker():
                    # this will terminate the bfs
                    # as we have previously drained the Queue
                    # and we are not going to append anything new
                    return unique_links

                local_seen.add(link)
                bfs_queue.append(link)
                unique_links.append(link)

        if len(bfs_queue) != 0:
            bfs_queue.append(SENTINEL)

        return unique_links
