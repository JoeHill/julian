# -*- coding: utf-8 -*-
import sys
import re 

from discourse.api.services.db import node
from discourse.api.models.node import Node

from discourse.api import note
from discourse.api import edge

from discourse.api.services.nltk import pos

def get_from_note_id(note_id):
    """
    Parses the string in a note and returns the proper noun phrases representing nodes.

    """
    n, errors = note.find_by_id(note_id)
    s = n.prioritya + u' ' + n.priorityb + u' ' + n.priorityc + u' ' + n.priorityd + u' ' + n.prioritye
    res, errs = get_from_string(s)
    return res, errs + errors

def get_from_note(n):
    """
    Parses the note into nodes.
    """
    s = n.prioritya + u' ' + n.priorityb + u' ' + n.priorityc + u' ' + n.priorityd + u' ' + n.prioritye
    res, errs = get_from_string(s)
    return res, errs

def get_from_string(s):
    """
    Parses a string into a list of POS tagged tuples. After that parses out all proper nouns. If the NNP is followed by another NNP they are concatenated.
    
    :param str string: The string to parse. It's assumed the string is proper English.
    
    :rtype list(str): The list of proper nouns
    """
    models = []
    errors = []
    try:
        unigrams = re.split("\s+", s)
        for unigram in unigrams:
            models.append(Node(title=unigram, note_id=-1))
            
        return models, errors
    except:
        return [], [sys.exc_info()] + errors

def create_from_note_id(note_id):
    """
    Creates a set of nodes in the database from a note that is already stored.
    
    :param note_id: The id of the note
    
    """
    try:
        errors = []
        new_nodes = []
        nodes, errors = get_from_note_id(note_id)
        for n in nodes:
            res, errors = get_or_create_by_title_and_note_id( n.title, note_id )
            new_node, created = res
            if created:
                new_nodes.append( new_node )
        return new_nodes, errors
    except:
        return [], [sys.exc_info()] + errors

def get_or_create_by_title_and_note_id(node_title, note_id=-1):
    """
    Gets or creates a node from a title
    
    :param str node_title: The title of the Node
    :param int note_id: The id of the originating note.
    
    :rtype Node, [errors]
    """
    try:
        res, errors = node.get_or_create_by_title_and_note_id(node_title, note_id)
        n, created = res
        return ( db_to_model(n), created ), errors
    except:
        return ( None, False ), [sys.exc_info()] + errors

def find_stored_by_note_id(note_id):
    """
    If the note has been parsed this method will return the Nodes in the note. If not it will return unsaved Nodes for the note by parsing it.
    
    :param int note_id: The id for the note
    
    :rtype Note, [Errors]
    """
    ns, errors = node.find_by_note_id(note_id)
    return [db_to_model(n) for n in ns], errors

def find_by_ids(node_ids):
    """
    Returns a unique list of nodes given a list of node ids.
    
    :param list(int) node_ids: The ids of the nodes.
    
    :rtype list(Node), (Error):
    """
    ns, errors = node.find_by_ids(node_ids)
    return [db_to_model(n) for n in ns], errors

def find():
    """
    Returns all nodes stored locally.
    
    """
    ns, errors = node.find()
    return [db_to_model(n) for n in ns], errors

def db_to_model(o):
    if not o:
        raise Exception("Object not passed to convert to model")
    return Node(id=o.id,
                title=o.title,
                note_id=o.note_id)
