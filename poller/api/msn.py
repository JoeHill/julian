from poller.services.msnpoller import MsnPoller

def poll():
    """
    Runs the poller for MSN
    
    """
    p = MsnPoller()
    pages =  p.fetch_pages()
    for url, html in pages:
        p.process_as_rss( html )