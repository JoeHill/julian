from julian.discourse.services.db import note
from julian.discourse.api.models.note import Note

def exists( identifier ):
    """
    Determines whether a note corresponding to a particular identifier exists already.
    
    :param str identifier: The identifier for the note.
    
    :rtype bool:
    """
    return note.exists(identifier)

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
    return ( db_to_model(n), created ), errors

def db_to_model(o):
    if not o:
        raise Exception( "Object not passed to convert to Model" )
    return Note(
        identifier   = o.identifier,
        prioritya    = o.prioritya,
        priorityb    = o.priorityb,
        priorityc    = o.priorityc,
        priorityd    = o.priorityd,
        prioritye    = o.prioritye,
        created_at   = o.created_at,
        updated_at   = o.updated_at,
        published_at = o.published_at
    )