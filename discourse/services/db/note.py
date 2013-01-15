import sys

from julian.discourse.models import Note

from julian.utils import UNDEFINED
from julian.utils import SentinelValue as SV

def exists(identifier):
    """
    Determines whether a note corresponding to a particular identifier exists already.
    
    :param str identifier: The identifier for the note.
    
    :rtype bool:
    """
    try:
        n = Note.objects.all().filter(identifier=identifier)
        if n and n[0]:
            return True
    except:
        return False
    return False

def find_all_unprocessed():
    """
    Returns a list of all notes.
    
    :rtype [Note], [Errors]
    """
    try: 
        return Note.objects.all().filter(processed=False), []
    except:
        return None, [sys.exc_info()]
    
def update( id=UNDEFINED, identifier=UNDEFINED, prioritya=UNDEFINED, priorityb=UNDEFINED, priorityc=UNDEFINED, priorityd=UNDEFINED, prioritye=UNDEFINED, created_at=UNDEFINED, updated_at=UNDEFINED, published_at=UNDEFINED, processed=UNDEFINED):
    """
    Updates a note given the parameters passed.
    
    :param int id: The primary key of the note. Either this or the identifier string is required.
    :param str identifier: A unique identifier for the note. Either this or the id is required.
    :param str prioritya: Text to parse at a later time.
    :param str priorityb: Text to parse at a later time.
    :param str priorityc: Text to parse at a later time.
    :param str priorityd: Text to parse at a later time.
    :param str prioritye: Text to parse at a later time.    
    :param datetime created_at: The time this note was created in the db.
    :param datetime updated_at: The last time this note was updated.
    :param datetime published_at: The date this note was published online
    :param bool processed: Whether or not the note has been picked up and processed
    
    :rtype Note, [Errors]
    """
    try:
        params = dict( filter( lambda i: not isinstance( i, SV ), locals().items() ) )

        pk = params['id']
        del params['id']
        
        n = Note.objects.get( pk=pk )
        for key, val in params.items():
            setattr( n, key, val )
        n.save()
        
        return n, []
    except:
        return None, [sys.exc_info()]
        

def find_by_id( note_id ):
    """
    Finds a note by id.
    
    :param int note_id: The id for the note
    
    :rtype Note, [Errors]:
    """
    try:
        return Note.objects.get( pk=note_id ), []
    except:
        return None, [sys.exc_info()]

def get_or_create(identifier='', prioritya="", priorityb="", priorityc="", priorityd="", prioritye="", published_at=None):
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
        notes = Note.objects.all().filter(identifier=identifier)
        if notes:
            note = notes[0]
            created = False
        if not note:
            note = Note.objects.create(identifier=identifier,
                                         prioritya=prioritya,
                                         priorityb=priorityb,
                                         priorityc=priorityc,
                                         priorityd=priorityd,
                                         prioritye=prioritye,
                                         published_at=published_at)
            if note:
                created = True
        return (note, created), []
    except:
        return (None, None), [sys.exc_info()]
