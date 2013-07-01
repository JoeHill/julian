import sys

from discourse.models import Edge

def find_by_note_id(note_id):
    """
    Finds Edges by the note id.
    
    :param int note_id: The id for the note
    
    :rtype list(Edge), (Error)
    """
    try:
        es = Edge.objects.all().filter(note_id=note_id)
        return es, []
    except:
        return None, [sys.exc_info()]
    
