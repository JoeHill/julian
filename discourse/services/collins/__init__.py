def pos_tagged_to_collins_tree( tagged_string ):
    """
    Converts a sentence tagged by the NLTK to a string parsable by the Collins' parser
    
    :param list(tuple(str,str)) tagged_sentence: The sentence that has been tagged by the NLTK with pos annotations.
    
    :rtype str: A string the Collins' parser can parse
    """
    