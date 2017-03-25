"""
An asynchronous implementation of the RequestsExecutor
"""
import grequests
import multiprocessing

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from BaseRequestsExecutor import BaseRequestsExecutor


class RequestsExecutorAsync(BaseRequestsExecutor):

    def __init__(self, timeout=3):
        super(RequestsExecutorAsync, self).__init__(timeout)

    def send_requests(self, list_requests):
        threads_count = multiprocessing.cpu_count()

        # 408 Request Timeout
        retry = Retry(total=2, backoff_factor=0.2, status_forcelist=[408], raise_on_redirect=True)

        session = grequests.Session()
        session.mount('http://', HTTPAdapter(max_retries=retry))
        session.mount('https://', HTTPAdapter(max_retries=retry))

        responses = [grequests.get(link, timeout=self.timeout, session=session) for link in list_requests]
        return grequests.imap(responses, size=threads_count * 4, exception_handler=self.handle_exceptions)

