from poller.services.aljazeerapoller import AlJazeeraPoller

def poll():
    """
    Runs the poller for the New York Times
    
    """
    p = AlJazeeraPoller()
    pages =  p.fetch_pages()
    for url, html in pages:
        p.process_as_rss( html )