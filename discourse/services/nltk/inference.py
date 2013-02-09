import nltk

def role( tree_component ):
    """
    Returns True if the component of the tree is relevant to an edge.
    
    :param tuple/nltk.tree.Tree tree_component: A component of a nltk.tree.Tree
    
    :rtype bool:
    """
    if isinstance( tree_component, nltk.tree.Tree ):
        if tree_component.node in ( 'NP', 'VP' ):
            return 'np'
    if isinstance( tree_component, tuple ):
        if tree_component[1] in ( 'VB',   # base
                                  'VBZ',  # 3rd singular present
                                  'VBN',  # past participle
                                  'VBG',  # gerund
                                  'VBD'): # simple past
            return 'verb'
    return False
        
        
        
def deduce_edges_from_tree(tree):
    """
    Deduces relationships between noun phrases in a tree.
    
    :param nltk.tree.Tree tree: The tree from which to deduce relationships.
    
    :rtype tuple(str, str, str): A tuple containing the first noun phrase, the relationship or action, and the noun phrase receiving the action.
    """
    components = filter( role, tree )
    for st in components:
        print "COMPONENT", role( st ), st