import sys

from julian.discourse.services.db import note
from julian.discourse.api.models.note import Note

from julian.utils import UNDEFINED
from julian.utils import SentinelValue as SV

def exists( identifier ):
    """
    Determines whether a note corresponding to a particular identifier exists already.
    
    :param str identifier: The identifier for the note.
    
    :rtype bool:
    """
    return note.exists(identifier)

def find_by_id( note_id ):
    """
    Finds the note by id.
    
    :param int id: The id for the note
    
    :rtype Note, [Errors]
    """
    n, errors = note.find_by_id( note_id )
    if errors:
        print errors
    try:
        return db_to_model(n), errors
    except:
        return None, [sys.exc_info()]

def find_by_start_date_and_end_date(start_date, end_date):
    """
    Finds notes by the published_at date range.
    
    :param datetime.datetime start_date: The starting date for the note.
    :param datetime.datetime end_date: The ending date for the note.
    
    :rtype list(julian.discourse.api.models.Note):
    """
    try:
        ns, errors = note.find_by_start_date_and_end_date(start_date, end_date)
        return [db_to_model(n) for n in ns], errors
    except:
        return None, [sys.exc_info()]
    
def update( id=UNDEFINED, identifier=UNDEFINED, prioritya=UNDEFINED, priorityb=UNDEFINED, priorityc=UNDEFINED, priorityd=UNDEFINED, prioritye=UNDEFINED, created_at=UNDEFINED, updated_at=UNDEFINED, published_at=UNDEFINED, processed=UNDEFINED):
    """
    Updates a note given the parameters passed.
    
    :param int id: The primary key of the note. Required.
    :param str identifier: A unique identifier for the note.
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
    errors = []
    params = dict( filter( lambda i: not isinstance( i, SV ), locals().items() ) )
    if 'id' not in params:
        return None, [("'id' is a required parameter to update", None, None)]
    n, errors = note.update( **params )
    try:    
        return db_to_model(n), errors
    except:
        return None, [sys.exc_info()] + errors
    

def find_all_unprocessed():
    """
    Returns a list of all notes.
    
    :rtype [Note], [Errors]
    """
    ns, errors = note.find_all_unprocessed()
    try:
        return [db_to_model(n) for n in ns], errors
    except:
        return [], [sys.exc_info] + errors

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
    note_created, errors = note.get_or_create(identifier=identifier, 
                                              prioritya=prioritya, 
                                              priorityb=priorityb, 
                                              priorityc=priorityc, 
                                              priorityd=priorityd, 
                                              prioritye=prioritye, 
                                              published_at=published_at)
    n, created = note_created
    try:
        return ( db_to_model(n), created ), errors
    except:
        return ( None, False ), errors

def db_to_model(o):
    if not o:
        raise Exception( "Object not passed to convert to Model" )
    return Note(
        id           = o.id,
        identifier   = o.identifier,
        prioritya    = o.prioritya,
        priorityb    = o.priorityb,
        priorityc    = o.priorityc,
        priorityd    = o.priorityd,
        prioritye    = o.prioritye,
        created_at   = o.created_at,
        updated_at   = o.updated_at,
        published_at = o.published_at,
        processed    = o.processed
    )