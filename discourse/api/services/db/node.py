import sys

from discourse.models import Edge
from discourse.models import Node

def find():
    """
    Finds all nodes stored locally
    
    """
    try:
        nodes = []
        return [n for n in Node.objects.all()], []
    except:
        return [], [sys.exc_info()]
        

def find_by_note_id(note_id):
    """
    If the note has been parsed this method will return the Nodes in the note. If not it will return unsaved Nodes for the note by parsing it.
    
    :param int note_id: The id for the note
    
    :rtype Note, [Errors]
    """
    try:
        node_ids = []
        es = Edge.objects.all().filter(note_id=note_id)
        node_ids += [ es.from_node_id, es.to_node_id ]
        node_ids = list( set( node_ids ) )
        nodes, errors = find_by_ids( node_ids ) 
        return es, errors
    except:
        return None, [sys.exc_info()]
    
def get_or_create_by_title_and_note_id(node_title, note_id=-1):
    """
    Gets or creates a node from a title
    
    :param str node_title: The title of the Node
    :param int note_id: The id of the originating note.
    
    :rtype Node, [errors]
    """
    try:
        n, created = Node.objects.get_or_create(title=node_title, 
                                                note_id=note_id)
        return ( n, created ), []
    except:
        return ( None, False ), [sys.exc_info()]
        
def find_by_ids(node_ids):
    """
    Returns a unique list of nodes given a list of node ids.
    
    :param list(int) node_ids: The ids of the nodes.
    
    :rtype list(Node), (Error):
    """
    try:
        ns = Node.objects.all().filter(pk__in=node_ids)
        return ns, []
    except:
        return None, [sys.exc_info()]