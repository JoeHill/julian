from julian.discourse.services.db import note

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
    return note.get_or_create(**locals())

