import unittest

from poller.services.nytpoller import NytPoller

class PollerTest( unittest.TestCase ):

    def test_init(self):
        p = NytPoller()
        pages =  p.fetch_pages()
        for url, html in pages:
            p.process_as_rss( html )