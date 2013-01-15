from julian.poller.services.aljazeerapoller import AlJazeeraPoller
from julian.poller.services.huffpopoller import HuffPoPoller
from julian.poller.services.msnpoller import MsnPoller
from julian.poller.services.nytpoller import NytPoller
from julian.poller.services.usatodaypoller import UsaTodayPoller

def poll():
    AlJazeeraPoller().poll()
    HuffPoPoller().poll()
    MsnPoller().poll()
    NytPoller().poll()
    UsaTodayPoller().poll()