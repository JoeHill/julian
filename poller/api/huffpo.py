from poller.services.huffpopoller import HuffPoPoller

def poll():
    """
    Runs the poller for the Huffington Post
    
    """
    p = HuffPoPoller()
    pages =  p.fetch_pages()
    for url, html in pages:
        p.process_as_rss( html )