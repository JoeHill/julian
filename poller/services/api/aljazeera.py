from poller.services.aljazeerapoller import AlJazeeraPoller

def poll():
    """
    Runs the poller for the New York Times
    
    """
    AlJazeeraPoller().poll()