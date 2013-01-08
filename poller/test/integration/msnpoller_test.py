import unittest
import sys

from poller.services.msnpoller import MsnPoller

class PollerTest( unittest.TestCase ):

    def test_fetch(self):
        p = MsnPoller()
        pages =  p.fetch_pages()
        for url, html in pages:
            p.process_as_rss( html )