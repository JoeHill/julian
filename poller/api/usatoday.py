from poller.services.usatodaypoller import UsaTodayPoller

def poll():
    """
    Runs the poller for USA Today
    
    """
    p = UsaTodayPoller()
    pages =  p.fetch_pages()
    for url, html in pages:
        p.process_as_rss( html )