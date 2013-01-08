from poller.services.huffpopoller import HuffPoPoller

def poll():
    """
    Runs the poller for the Huffington Post
    
    """
    HuffPoPoller().poll()