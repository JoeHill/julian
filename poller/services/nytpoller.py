import sys
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