"""
RequestsOrchestrator manages the way we send requests
"""

from abc import ABCMeta, abstractmethod


class BaseRequestsExecutor(object):

    __metaclass__ = ABCMeta

    def __init__(self, timeout):
        self.timeout = timeout

    def handle_exceptions(self, request, exception):
        # TODO: log it instead of printing to sdout
        print str(request.url) + ' failed with: ' + str(exception)

    @abstractmethod
    def send_requests(self, list_requests):
        pass
