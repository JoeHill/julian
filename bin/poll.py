#!which python

import sys
import os

def poll():
    nyt.poll()
    usatoday.poll()
    
if __name__ == '__main__':
    abspath = os.path.abspath(__name__).replace( '__main__', '' )

    sys.path.append(abspath)
    sys.path.append(abspath.replace('julian/', ''))
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'julian.settings'
    os.environ['USE_CALIENDO'] = 'True'
    
    from julian.poller.api import nyt
    from julian.poller.api import usatoday
    
    poll()