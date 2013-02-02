import unittest

from discourse.services.nltk import inference
from discourse.services.nltk import pos

class TestInference(unittest.TestCase):
    
    def test_simple_deduce_edges_from_tree(self):
        s = "The boy threw the ball.  Adam wears a blue hat.  Barack Obama is the president."
        sentences = pos.tag(s)
        trees = []
        for sentence in sentences:
            trees += [pos.np_chunker.parse(sentence)]

        for tree in trees:
            print "TREE", tree
            inference.deduce_edges_from_tree(tree)
            
        assert False

    def test_complex_deduce_edges_from_tree(self):
        pass
        """
        s = "The boy threw the ball. Adam wears a blue hat. Barack Obama is the president."
        sentences = pos.tag(s)
        trees = []
        for sentence in sentences:
            trees += [pos.parser.parse(sentence)]

        for tree in trees:
            inference.deduce_edges_from_tree(tree)
            
        assert False
        """
        
if __name__ == '__main__':
    unittest.main()