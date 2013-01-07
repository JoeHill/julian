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
        #"http://rssfeeds.usatoday.com/usatoday-LifeTopStories", # Causes seg fault!? Check for regex issues.
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