import unittest
import sys

from poller.services.huffpopoller import HuffPoPoller

class PollerTest( unittest.TestCase ):

    def test_fetch(self):
        p = HuffPoPoller()
        pages =  p.fetch_pages()
        for url, html in pages:
            p.process_as_rss( html )