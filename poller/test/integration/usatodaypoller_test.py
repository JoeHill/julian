import unittest
import sys

from poller.services.usatodaypoller import UsaTodayPoller

class PollerTest( unittest.TestCase ):

    def test_fetch(self):
        p = UsaTodayPoller()
        pages =  p.fetch_pages()
        for url, html in pages:
            sys.stderr.write("Fetching url " + str(url) + "...\n")
            p.process_as_rss( html )