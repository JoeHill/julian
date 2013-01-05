import sys

from julian.discourse.models import Note

def exists( identifier ):
    """
    Determines whether a note corresponding to a particular identifier exists already.
    
    :param str identifier: The identifier for the note.
    
    :rtype bool:
    """
    try:
        n = Note.objects.all().filter( identifier=identifier )
        if n and n[0]:
            return True
    except:
        return False
    return False
        

def get_or_create( identifier='', prioritya="", priorityb="", priorityc="", priorityd="", prioritye="", published_at=None ):
    """
    Either fetches or creates a note from an identifier and set of attributes.
    
    :param str identifier: Something unique to this note so we don't save it twice
    :param str prioritya: Text to parse at a later time.
    :param str priorityb: Text to parse at a later time.
    :param str priorityc: Text to parse at a later time.
    :param str priorityd: Text to parse at a later time.
    :param str prioritye: Text to parse at a later time.
    
    :rtype tuple(tuple(<Note>, <bool>), tuple(<exec info>))
    """
    try:
        params = locals()
        note = None
        notes = Note.objects.all().filter( identifier=identifier )
        if notes:
            note = notes[0]
            created = False
        if not note:
            note = Note.objects.create( identifier=identifier,
                                         prioritya=prioritya,
                                         priorityb=priorityb,
                                         priorityc=priorityc,
                                         priorityd=priorityd,
                                         prioritye=prioritye,
                                         published_at=published_at )
            if note:
                created = True
        return ( note, created ), (None, None, None)
    except:
        return (None, None), sys.exc_info()