from julian.poller.services.aljazeerapoller import AlJazeeraPoller
from julian.poller.services.huffpopoller import HuffPoPoller
from julian.poller.services.msnpoller import MsnPoller
from julian.poller.services.nytpoller import NytPoller
from julian.poller.services.usatodaypoller import UsaTodayPoller
from julian.poller.services.south_carolina.standard_format import Standard

def poll():
    try:    
        AlJazeeraPoller().poll()
    except:
        pass
    
    try:
        HuffPoPoller().poll()
    except:
        pass
    
    try:
        MsnPoller().poll()
    except:
        pass
    
    try:
        NytPoller().poll()
    except:
        pass
    
    try:
        UsaTodayPoller().poll()
    except:
        pass
    
    try:
        Standard().poll()
    except:
        pass