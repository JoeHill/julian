from poller.services.msnpoller import MsnPoller

def poll():
    """
    Runs the poller for MSN
    
    """
    MsnPoller().poll()
