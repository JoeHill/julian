import nltk

from julian.discourse.services.db import edge

from julian.discourse.api.models.edge import Edge

def find_by_note_id(note_id):
    """
    Finds a list of edges by the note id.
    
    :param int note_id: The id of the note to find the edges in
    
    :rtype list(Edge), (Error):
    """
    es, errors = edge.find_by_note_id(note_id)
    return [db_to_model(e) for e in es], (None, None, None)

def create_from_note_and_nodes( note, nodes ):
    """
    Creates a set of edges given a note and a list of nodes.
    
    :param discourse.api.models.note.Note note: The note from which to create edges.
    :param list(discourse.api.models.node.Node) nodes: The list of nodes to discover edges for.
    
    :rtype list(discourse.api.models.edge.Edge): A list of edges for the nodes in the note.
    """
    # Semantically tag the note. 
    # Identify relationships with nodes.
    # Create edges
    
def db_to_model(o):
    if not o:
        raise Exception( "No object passed to convert to model." )
    return Edge( from_node_id = o.from_node_id,
                 to_node_id = o.to_node_id,
                 edge_type = o.edge_type,
                 discourse = o.discourse,
                 note = o.note )