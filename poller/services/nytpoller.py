import sys
import re
import time
import datetime

from poller.services.internals import Poller
from poller.services.exceptions import EmptyDOM
from poller.services.exceptions import NoDate

from discourse.api import note

class NytPoller( Poller ):

    rss_feeds = [
        "http://rss.nytimes.com/services/xml/rss/nyt/GlobalHome.xml",
        "http://atwar.blogs.nytimes.com/feed/",
        "http://www.nytimes.com/services/xml/rss/nyt/World.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/Africa.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/Americas.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/Europe.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/Education.xml",
        "http://thechoice.blogs.nytimes.com/feed",
        "http://learning.blogs.nytimes.com/feed",
        "http://www.nytimes.com/services/xml/rss/nyt/Politics.xml",
        "http://fivethirtyeight.blogs.nytimes.com/feed/",
        "http://thelede.blogs.nytimes.com/feed/",
        "http://feeds.nytimes.com/nyt/rss/Business",
        "http://norris.blogs.nytimes.com/feed/",
        "http://www.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
        "http://green.blogs.nytimes.com/feed/",
        "http://www.nytimes.com/services/xml/rss/nyt/GlobalBusiness.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml",
        "http://boss.blogs.nytimes.com/feed",
        "http://www.nytimes.com/services/xml/rss/nyt/Economy.xml",
        "http://economix.blogs.nytimes.com/feed/",
        "http://dealbook.blogs.nytimes.com/feed/",
        "http://www.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml",
        "http://mediadecoder.blogs.nytimes.com/feed",
        "http://www.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
        "http://bucks.blogs.nytimes.com/feed",
        "http://feeds.nytimes.com/nyt/rss/Technology",
        "http://bits.blogs.nytimes.com/feed/",
        "http://www.nytimes.com/services/xml/rss/nyt/business-computing.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/companies.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/internet.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/PersonalTech.xml",
        "http://gadgetwise.blogs.nytimes.com/feed/",
        "http://pogue.blogs.nytimes.com/feed/",
        "http://www.nytimes.com/services/xml/rss/nyt/start-ups.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/Science.xml",
        "http://www.nytimes.com/services/xml/rss/nyt/Environment.xml",
        "http://green.blogs.nytimes.com/feed/",
        "http://www.nytimes.com/services/xml/rss/nyt/Space.xml"
    ]

    def fetch_pages(self):
        for feed in self.rss_feeds:
            retries = 3
            feed_text = None 
            while not feed_text and retries > 0:
                try:
                    sys.stderr.write( "Getting text for feed: " + feed + "\n" )
                    feed_text = self.get( feed )
                    yield feed, feed_text
                except:
                    retries = retries - 1
                    sys.stderr.write( "Retrying for feed: " + feed + "\n" )
                
            #feed_dom  = self.parse()
      
    def articles(self):
        pass
    
    def get_datetime(self, published_at):
        # Sat, 05 Jan 2013 03:55:54 +0000
        if '+' in published_at:
            t = time.strptime( published_at, "%a, %d %b %Y %H:%M:%S +0000" )
        elif 'MT' in published_at:
            t = time.strptime( published_at, "%a, %d %b %Y %H:%M:%S %Z" )
        else:
            raise NoDate( "No date could be discerned from <pubdate>")

        year = t.tm_year
        month = t.tm_mon
        day = t.tm_mday
        hour = t.tm_hour
        minute = t.tm_min
        second = t.tm_sec
        return datetime.datetime( year=year, month=month, day=day, hour=hour, minute=minute, second=second )
    
    def process_as_rss(self, document):
        self.document = document
        self.parse()
        items = self.items()
        sys.stderr.write( "Pulling " + str(len(items)) + " articles...\n" )
        for item in items:
            pubdate = item.findAll('pubdate')
            published_at = self.get_datetime( pubdate.pop().get_text() )
            links = [ link.next_sibling for link in item.findAll( 'link' ) ]
            for link in links:
                if note.exists( link ):
                    sys.stderr.write( "Note exists...\n" )
                    continue
                try:
                    self.fetch_and_clean_dom( link )
                except EmptyDOM: # Server returned an empty response.
                    sys.stderr.write( "Empty DOM for link: " + link + ".\n" )
                    continue
                prioritya = ".  ".join( self.h1s() )
                priorityb = ".  ".join( self.h2s() )
                priorityc = ".  ".join( self.h3s() )
                priorityd = ".  ".join( [ a[0] for a in self.as_() ] )
                prioritye = " ".join( self.ps() )
                
                n, errors = note.get_or_create( link, prioritya, priorityb, priorityc, priorityd, prioritye, published_at )
                if errors[0]:
                    sys.stderr.write( str( errors ) + "\n" )