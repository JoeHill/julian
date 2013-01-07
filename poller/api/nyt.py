from poller.services.nytpoller import NytPoller

def poll():
    """
    Runs the poller for the New York Times
    
    """
    p = NytPoller()
    pages =  p.fetch_pages()
    for url, html in pages:
        p.process_as_rss( html )