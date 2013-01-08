from poller.services.nytpoller import NytPoller

def poll():
    """
    Runs the poller for the New York Times
    
    """
    NytPoller().poll()
