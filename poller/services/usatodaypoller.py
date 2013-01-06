import sys
import time
import datetime

from poller.services.internals import Poller
from poller.services.exceptions import EmptyDOM
from poller.services.exceptions import NoDate

from discourse.api import note

class UsaTodayPoller( Poller ):

    rss_feeds = [
        "http://rssfeeds.usatoday.com/usatoday-NewsTopStories",
        "http://rssfeeds.usatoday.com/UsatodaycomWorld-TopStories",
        "http://rssfeeds.usatoday.com/UsatodaycomNation-TopStories",
        "http://rssfeeds.usatoday.com/News-Opinion",
        "http://rssfeeds.usatoday.com/UsatodaycomWashington-TopStories",
        "http://rssfeeds.usatoday.com/usatoday-LifeTopStories",
        "http://rssfeeds.usatoday.com/UsatodaycomMovies-TopStories",
        "http://rssfeeds.usatoday.com/toppeople",
        "http://rssfeeds.usatoday.com/UsatodaycomMusic-TopStories",
        "http://rssfeeds.usatoday.com/UsatodaycomTelevision-TopStories",
        "http://rssfeeds.usatoday.com/UsatodaycomBooks-TopStories",
        "http://rssfeeds.usatoday.com/UsatodaycomMoney-TopStories",
        "http://rssfeeds.usatoday.com/UsatodaycomMoney-Healey",
        "http://rssfeeds.usatoday.com/usatoday-TechTopStories",
        "http://rssfeeds.usatoday.com/topgaming",
        "http://rssfeeds.usatoday.com/UsatodaycomTech-PersonalTalk",
    ]
      
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
        for item in items:
            pubdate = item.findAll('pubdate')
            published_at = self.get_datetime( pubdate.pop().get_text() )
            links = [ link.next_sibling for link in item.findAll( 'link' ) ]
            for link in links:
                if note.exists( link ):
                    continue
                try:
                    self.fetch_and_clean_dom( link )
                except EmptyDOM: # Server returned an empty response.
                    continue
                prioritya = ".  ".join( self.h1s() )
                priorityb = ".  ".join( self.h2s() )
                priorityc = ".  ".join( self.h3s() )
                priorityd = ".  ".join( [ a[0] for a in self.as_() ] )
                prioritye = " ".join( self.ps() )
                
                sys.stderr.write( "Creating note with identifier: " + str(link) + "\n" )
                n, errors = note.get_or_create( link, prioritya, priorityb, priorityc, priorityd, prioritye, published_at )
                if errors[0]:
                    sys.stderr.write( str( errors ) + "\n" )