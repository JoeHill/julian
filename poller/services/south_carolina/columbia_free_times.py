import sys

from poller.services.exceptions import EmptyDOM

from discourse.api import note

from poller.services.internals import Poller

class ColumbiaFreeTimes(Poller):
    
    rss_feeds = [ "http://www.free-times.com/site/rss_main"]
    
    def process_as_rss(self, document):
        self.document = document
        self.parse()
        items = self.items()
        for item in items:
            pubdate = item.findAll('dc:date')
            if not pubdate:
                continue
            published_at = self.get_datetime(pubdate.pop().get_text())
            links = [ link.next_sibling for link in item.findAll('link') ]
            for link in links:
                if not link or note.exists(link):
                    continue
                try:
                    self.fetch_and_clean_dom(link)
                except EmptyDOM: # Server returned an empty response.
                    continue
                prioritya = ".  ".join(self.h1s())
                priorityb = ".  ".join(self.h2s())
                priorityc = ".  ".join(self.h3s())
                priorityd = ".  ".join([ a[0] for a in self.as_() ])
                prioritye = " ".join(self.ps())
                
                n, errors = note.get_or_create(link, prioritya, priorityb, priorityc, priorityd, prioritye, published_at)
                if errors:
                    sys.stderr.write(str(errors) + "\n")
                