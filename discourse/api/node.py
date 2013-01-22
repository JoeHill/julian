# -*- coding: utf-8 -*-
import sys
import re 

import nltk
from nltk import tokenize
from nltk.chunk.regexp import RegexpParser

from julian.discourse.services.db import node
from julian.discourse.api import note

from julian.discourse.api.models.node import Node

def get_from_note_id(note_id):
    """
    Parses the string in a note and returns the proper noun phrases representing nodes.

    """
    n, errors = note.find_by_id(note_id)
    s = n.prioritya + u' ' + n.priorityb + u' ' + n.priorityc + u' ' + n.priorityd + u' ' + n.prioritye
    res, errs = get_from_string(s)
    return res, errs + errors

def get_from_string(s):
    """
    Parses a string into a list of POS tagged tuples. After that parses out all proper nouns. If the NNP is followed by another NNP they are concatenated.
    
    :param str string: The string to parse. It's assumed the string is proper English.
    
    :rtype list(str): The list of proper nouns
    """
    quoted = []
    unquoted = []
    subtrees = []
    models = []
    errors = []
    titles = set()
    try:
        sentences = tokenize.sent_tokenize(s)
        for sentence in sentences:
            if u'“' in sentence or u'”' in sentence or u'"' in sentence:
                quoted.append(sentence)
            else:
                unquoted.append(sentence)
            
        parser = RegexpParser("NP: {<DT>? <JJ>* <NN|NNP|NNS|CD>+}", loop=5) 
        for s in unquoted:
            parsed = parser.parse(nltk.pos_tag(s.split(' ')))
            subtrees += parsed.subtrees()
            
        subtrees = filter(lambda st: st.node == 'NP', subtrees)
        for tree in subtrees:
            title = re.sub(r"\s+", " ", " ".join([ word[0] for word in tree ])) # Replace multiple spaces with one
            title = re.sub(r"[^-. 'a-zA-Z]", "", title) # Clean punctuation
            title = re.sub(r"\.$", "", title) # Remove trailing periods
            title = re.sub(r"\s*$", "", title) # Strip right
            title = re.sub(r"^\s*", "", title) # Strip left 
            titles.add(title)
            
        for title in titles:
            models.append(Node(title=title))
        
        return models, errors
    except:
        return [], [sys.exc_info()] + errors

def create_from_note_id(note_id):
    """
    Creates a set of nodes in the database from a note that is already stored.
    
    :param note_id: The id of the note
    
    """
    try:
        new_nodes = []
        nodes, errors = get_from_note_id(note_id)
        for n in nodes:
            res, errors = get_or_create_by_title( n.title )
            new_node, created = res
            if created:
                new_nodes.append( new_node )
        return new_nodes, errors
    except:
        [], [sys.exc_info()] + errors

def get_or_create_by_title(node_title):
    """
    Creates a node from a title
    
    :param str node_title: The title of the Node
    
    :rtype Node, [errors]
    """
    res, errors = node.create_by_title(node_title)
    n, created = res
    try:
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

def db_to_model(o):
    if not o:
        raise Exception("Object not passed to convert to model")
    return Node(id=o.id,
                title=o.title)
