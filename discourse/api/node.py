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
    Parses a string into a list of POS tagged tuples. After that parses out all proper nouns. If the NNP is followed by another NNP they are concatenated.
    
    :param str string: The string to parse. It's assumed the string is proper English.
    
    :rtype list(str): The list of proper nouns
    """
    quoted = []
    unquoted = []
    subtrees = []
    models = []
    titles = set()
    n, errors = note.find_by_id(note_id)
    s = " ".join([n.prioritya, n.priorityb, n.priorityc, n.priorityd, n.prioritye])
    try:
        sentences = tokenize.sent_tokenize(s)
        for sentence in sentences:
            if '“' in sentence or '”' in sentence or '"' in sentence:
                quoted.append(sentence)
            else:
                unquoted.append(sentence)
                
        parser = RegexpParser("NP: {<DT>? <JJ>* <NN|NNP|NNS|CD>+}", loop=5 ) 
        for s in unquoted:
            parsed = parser.parse( nltk.pos_tag( s.split( ' ' ) ) )
            subtrees += parsed.subtrees()
            
        subtrees = filter( lambda st: st.node == 'NP', subtrees )
        for tree in subtrees:
            title = re.sub( r"\s+", " ", " ".join([ word[0] for word in tree ]) )
            title = re.sub( r"[^-. 'a-zA-Z]", "", title ) # Clean punctuation
            title = re.sub( r"\.$", "", title )
            titles.add( title )
            
        for title in titles:
            models.append(Node( title=title ) )
        
        return models, errors
    except:
        return None, [sys.exc_info()] + errors

def create_by_title(node_title):
    """
    Creates a node from a title
    
    :param str node_title: The title of the Node
    
    :rtype Node, [errors]
    """
    n, errors = node.create_by_title(node_title)
    try:
        return db_to_model(n), errors
    except:
        return None, [sys.exc_info()]

def find_by_note_id( note_id ):
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
        raise Exception( "Object not passed to convert to model" )
    return Node(id=o.id,
                title=o.title)