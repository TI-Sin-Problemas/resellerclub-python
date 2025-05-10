"""Mock requests for testing purposes"""

import requests


class MockRequests:
    """Mock Requests class"""

    def __init__(self, response_content: bytes):
        r = requests.Response()
        r.encoding = "UTF-8"
        r.status_code = 200
        r._content = response_content
        self.response = r

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Get mock response from API"""
        return self.response

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Post mock response from API"""
        return self.response
