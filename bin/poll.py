#!/usr/bin/env python

import sys
import os

def poll():
    nyt.poll()
    usatoday.poll()
    aljazeera.poll()
    huffpo.poll()
    msn.poll()
    
if __name__ == '__main__':
    abspath = os.path.abspath(__file__)

    sys.path.append(abspath.replace('/bin/poll.py', ''))
    sys.path.append(abspath.replace('/julian/bin/poll.py', ''))
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'julian.settings'
    os.environ['USE_CALIENDO'] = 'True'
    
    from julian.poller.api import nyt
    from julian.poller.api import usatoday
    from julian.poller.api import aljazeera
    from julian.poller.api import huffpo
    from julian.poller.api import msn
    
    poll()