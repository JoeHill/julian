import sys
from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import Declaration

from poller.services.internals import Poller

from caliendo.facade import Facade

class NytPoller( Poller ):

  rss_feeds = [
    #"http://rss.nytimes.com/services/xml/rss/nyt/GlobalHome.xml", Resource not found
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
    feeds = [ ]
    for feed in self.rss_feeds:
      retries = 3
      feed_text = None 
      while not feed_text and retries > 0:
        try:
          sys.stderr.write( "Getting text for feed: " + feed + "\n" )
          feed_text = self.get( feed )
        except:
          retries = retries - 1
          sys.stderr.write( "Retrying for feed: " + feed + "\n" )

      #feed_dom  = self.parse()
      feeds.append( ( feed, feed_text ) )
    return feeds
      
  def articles(self):
    pass


def parse_rss(document):
    p = Poller()
    print "parse rss called."
    page = BeautifulSoup( document )
    items = page.findAll( 'item' )
    print "FOUND " + str( len( items ) ) + " items"
    for item in items:
      print "================================================"
      #print "Title:"
      #print [ title.text for title in item.findAll( 'title' ) ]
      #print "Link:"
      links = [ link.next_sibling for link in item.findAll( 'link' ) ]
      for link in links:
        linked_page = BeautifulSoup( p.get( link ) )
        #extracted_scripts = [ script.extract() for script in linked_page.findAll( 'script' ) ]
        dtds = [ dtd.extract() for dtd in linked_page.findAll( text=lambda text:isinstance( text, Declaration ) ) ]
        comments = [ comment.extract( ) for comment in linked_page.findAll(text=lambda text:isinstance(text, Comment)) ]
        scripts = [ script.extract() for script in linked_page.findAll( 'script' ) ]
        print "FOUND " + str( len( comments ) ) + " comments"

        print linked_page.get_text()
      #print "Comments:"
      #print [ comment.text for comment in item.findAll('comments') ]
      #print "pubdate: "
      #print [ pubdate.text for pubdate in item.findAll('pubdate')]
      #print "================================================"


if __name__ == '__main__':
  p = Facade( NytPoller() )
  pages =  p.fetch_pages( )
  url, html = pages[1]
  page = BeautifulSoup( html )
  print "About to parse rss..."
  parse_rss( html )
  print "Done parsing rss.'"