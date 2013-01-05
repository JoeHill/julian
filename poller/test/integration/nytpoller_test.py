import unittest

from poller.services.nytpoller import NytPoller

class PollerTest( unittest.TestCase ):

    def setUp(self):
        pass

    def test_init(self):
        p = NytPoller()
        pages =  p.fetch_pages()
        for url, html in pages:
            print "About to parse rss..."
            p.process_as_rss( html )
            print "Done parsing rss.'"


    def test_get(self):
        import pycurl
        import StringIO
        url = 'http://www.nytimes.com/2013/01/06/world/asia/travel-disrupted-in-china-amid-unusually-cold-weather.html?partner=rss'
        html = StringIO.StringIO( )
        curl = pycurl.Curl( )
        curl.setopt( pycurl.URL, url )
        curl.setopt( pycurl.FOLLOWLOCATION, True )
        curl.setopt( pycurl.MAXREDIRS, 100 )
        curl.setopt( pycurl.VERBOSE, True )
        curl.setopt( pycurl.CONNECTTIMEOUT, 30 )
        curl.setopt( pycurl.TIMEOUT, 100 )
        curl.setopt( pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1' )
        curl.setopt( pycurl.COOKIEFILE, 'cookie.txt' )
        curl.setopt( pycurl.COOKIEJAR       , 'cookie.txt' )
        curl.setopt( pycurl.NOSIGNAL, True )
        curl.setopt( pycurl.WRITEFUNCTION, html.write )
        curl.perform()
        document = html.getvalue()
        print "GOT DOCUMENT:", document
        assert document
