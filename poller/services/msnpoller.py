import sys

from poller.services.internals import Poller

from poller.services.exceptions import EmptyDOM

from discourse.api import note

class MsnPoller( Poller ):

    rss_feeds = [
        "http://msn.com/rss/news.aspx",
        "http://www.msn.com/rss/MsnEntertainment.aspx",
        "http://msn.com/rss/msnmoney.aspx",
        "http://msn.com/rss/sports.aspx",
        "http://www.msn.com/rss/searchabstract.aspx",
        "http://www.msn.com/rss/msnshopping_top.aspx",
        "http://money.msn.com/money-week.aspx",
        "http://money.msn.com/InvestingDepartment.aspx",
        "http://money.msn.com/Everything.aspx",
        "http://money.msn.com/jim-jubak-rss.aspx",
        "http://money.msn.com/liz-weston-rss.aspx",
        "http://autos.msn.com/xml/articles/rss/articles.xml",
        "http://autos.msn.com/xml/articles/rss/reviews.xml",
        "http://msn.careerbuilder.com/RTQ/rss20.aspx?rssid=msn_rssj",
        "http://msn.careerbuilder.com/Harvest/RSS/RSSArticleFeed.aspx?type=MSN&count=5&category=JOBSRCH",
        "http://msn.careerbuilder.com/Harvest/RSS/RSSArticleFeed.aspx?type=MSN&count=5&category=CVLTRES",
        "http://msn.careerbuilder.com/Harvest/RSS/RSSArticleFeed.aspx?type=MSN&count=5&category=INTRVW",
        "http://msn.careerbuilder.com/Harvest/RSS/RSSArticleFeed.aspx?type=MSN&count=5&category=SALPRO",
        "http://msn.careerbuilder.com/Harvest/RSS/RSSArticleFeed.aspx?type=MSN&count=5",
        "http://movies.msn.com/rss/entnews",
        "http://feeds.wonderwall.com/rss/msn_one_hot_gossip.xml",
        "http://movies.msn.com/rss/topphotogalleries",
        "http://movies.msn.com/rss/topmovienews/",
        "http://music.msn.com/rss/topmusicnews/",
        "http://tv.msn.com/rss/toptvnews/",
        "http://feeds.wonderwall.com/rss/wall.xml",
        "http://feeds.wonderwall.com/rss/shortlistgallery.xml",
        "http://healthyliving.msn.com/HotTopicsRSS",
        "http://healthyliving.msn.com/HealthNewsRSS",
        "http://autos.msn.com/xml/re/articles/rss/latestarticles_rss.xml",
        "http://autos.msn.com/xml/re/articles/rss/MoreFromMSNRealEstate_MostRecent.xml",
        "http://shopping.msn.com/xml/xmlresults/shp/?bcatid=4445,format=rss",
        "http://shopping.msn.com/xml/xmlresults/shp/?bCatID=4634,format=rss",
        "http://shopping.msn.com/xml/xmlresults/shp/?bCatID=6492,format=rss",
        "http://shopping.msn.com/xml/xmlresults/shp/?bCatID=4506,format=rss",
        "http://shopping.msn.com/xml/xmlresults/shp/?bCatID=4234,format=rss"
    ]