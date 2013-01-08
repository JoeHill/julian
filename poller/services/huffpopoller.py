import sys

from poller.services.internals import Poller

from poller.services.exceptions import EmptyDOM

from discourse.api import note

class HuffPoPoller( Poller ):

    rss_feeds = [
        "http://feeds.huffingtonpost.com/huffingtonpost/raw_feed",
        "http://feeds.huffingtonpost.com/huffingtonpost/LatestNews",
        "http://feeds.huffingtonpost.com/huffingtonpost/TheBlog",
        "http://feeds.huffingtonpost.com/HP/MostPopular",
        "http://www.huffingtonpost.com/tag/huffpolitics/feed",
        "http://www.huffingtonpost.com/feeds/verticals/politics/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/media/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/business/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/entertainment/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/entertainment/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/crime/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/dc/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/living/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/los-angeles/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/chicago/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/new-york/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/denver/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/world/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/sports/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/technology/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/books/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/food/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/religion/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/travel/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/college/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/impact/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/arts/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/healthy-living/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/divorce/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/san-francisco/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/education/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/celebrity/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/culture/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/own/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/money/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/women/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/parents/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/black-voices/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/latino-voices/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/small-business/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/weird-news/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/most_popular_entries/index.xml",
        "http://www.huffingtonpost.com/feeds/original_posts/index.xml",
        "http://www.huffingtonpost.com/wires/full_index.rdf",
        "http://www.huffingtonpost.com/feeds/verticals/weddings/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/50/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/gay-voices/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/high-school/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/college/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/taste/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/mindful-living/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/health-fitness/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/health-news/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/detroit/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/miami/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/tv/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/science/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/good-news/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/teen/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/gps-for-the-soul/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/huffpost-home/index.xml",
        "http://www.huffingtonpost.com/feeds/verticals/tedweekends/index.xml"
    ]
    
    def process_as_rss(self, document):
        self.document = document
        self.parse()
        items = self.entries()
        for item in items:
            pubdate = item.findAll('published')
            published_at = self.get_datetime( pubdate.pop().get_text() )
            links = []
            for link in item.findAll('link'):
                try:
                    links.append(link['href'])
                except:
                    pass
            for link in links:
                if not link or note.exists( link ) or 'jpg' in link:
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
                n, errors = note.get_or_create( link, prioritya, priorityb, priorityc, priorityd, prioritye, published_at )
                if errors[0]:
                    sys.stderr.write( str( errors ) + "\n" )