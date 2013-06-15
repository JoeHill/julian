#!/usr/bin/env python

import traceback
import sys
import os

if __name__ == '__main__':
    abspath = os.path.dirname(os.path.abspath(__file__))
    
    sys.path.append(os.path.join(abspath, '..'))
    sys.path.append(os.path.join(abspath, '..', '..'))
        
    os.environ['DJANGO_SETTINGS_MODULE'] = 'julian.settings'
    os.environ['USE_CALIENDO'] = 'True'
    
    import datetime
    
    from julian.discourse.api import note
    from julian.discourse.api import node
    
    today = datetime.datetime.now()
    
    notes, errors = note.find_by_start_date_and_end_date(start_date=today-datetime.timedelta(days=1), 
                                                 end_date=today)    
    
    print "Found %s new notes..." % len(notes)
    for n in notes:
        new_nodes, errors = node.create_from_note_id(n.id)
        print "Created %s new nodes..." % len(new_nodes)
        if errors:
            for e in errors:
                tb = e[2]
                traceback.print_tb(e[2])

