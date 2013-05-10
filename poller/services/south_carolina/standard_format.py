from poller.services.internals import Poller

class Standard(Poller):
    
    rss_feeds = ["http://www.postandcourier.com/section/pc&template=RSS&mime=xml", # Post and Courier
                 "http://www.scpress.org/rss.rss", # SC Press Association
                 "http://www.aikenstandard.com/section/RSS01?mime=xml", # Aiken Standard
                 # "http://www.independentmail.com/rss/headlines/news/" # Anderson Indepenent-Mail, requires subscription
                 "http://www.islandpacket.com/news/local/v-highlights/index.rss", # Beaufort Gazette
                 "http://www.charlestonbusiness.com/news/all/rss_view.xml", # Charleston Business Journal
                 # Bluffton today (Carolina morning news) has no RSS feed.
                 "http://www.charlestoncitypaper.com/charleston/Rss.xml", #  Charleston City Paper
                 # Chronicle Independent has no RSS feed
                 "http://www.thecolumbiastar.com/current/Front_Page/feed", # The columbia star
                 "http://www.gsabusiness.com/news/all/rss_view.xml", # Greenville business
                 "http://www.gaffneyledger.com/news.xml", # Gaffney Ledger
                 "http://www.greenvilleonline.com/section/NEWS&template=rss_gd&mime=xml", # Greenville Online
                 "http://www.islandpacket.com/news/local/v-highlights/index.rss", # island packet (Hilton Head)
                 #"http://www.thelancasternews.com/todaysnews/rss.xml", # Lancaster Requires subscription
                 "http://www.scnow.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss",
                 "http://uniondailytimes.com/rss/home/all+articles?content_type=article&page_name=home&offset=0&limit=200&instance=all+articles" # Union daily times
                  ]