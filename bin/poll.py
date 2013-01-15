#!/usr/bin/env python

import sys
import os

if __name__ == '__main__':
    abspath = os.path.abspath(__file__)

    sys.path.append(abspath.replace('/bin/poll.py', ''))
    sys.path.append(abspath.replace('/julian/bin/poll.py', ''))
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'julian.settings'
    os.environ['USE_CALIENDO'] = 'True'
    
    from julian.poller.services.api import poller
        
    poller.poll()