from poller.services.usatodaypoller import UsaTodayPoller

def poll():
    """
    Runs the poller for USA Today
    
    """
    UsaTodayPoller().poll()
    