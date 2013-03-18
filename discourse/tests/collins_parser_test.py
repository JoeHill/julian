import unittest

from nltk.draw.tree import draw_trees

import sys

from discourse.services.nltk import pos
from discourse.services.collins import parser

class TestCollinsParser(unittest.TestCase):

    def test_collins_to_tree(self):
        """
        s = "(TOP~is~1~1 (S~is~2~2 (NP-A~brother~2~1 (NPB~brother~2~2 My/PRP$ brother/NN ,/PUNC, ) (NP~Adam~2~1 Adam/NP ,/PUNC, (SBAR~who~2~1 (WHNP~who~1~1 who/WP ) (SG-A~finished~2~2 (ADVP~just~1~1 just/RB ) (VP~finished~2~1 finished/VBD (NPB~dissertation~2~2 his/PRP$ dissertation/NN ,/PUNC, ) ) ) ) ) ) (VP~is~2~1 is/VBZ (VP-A~headed~2~1 headed/VBN (PP~to~2~1 to/TO (NP-A~Rock~2~1 (NPB~Rock~2~2 Red/NNP Rock/NNP ,/PUNC, ) (NP~Carolina~2~1 (NPB~Carolina~2~2 South/NNP Carolina/NNP ) (NPB~weekend~2~2 this/DT weekend/NN ./PUNC. ) ) ) ) ) ) ) ) "
        sys.stderr.write( s + '\n')
        tree = parser.collins_to_tree(s)
        """
        pass
        
    def test_pos_tagged_to_collins_tree(self):
        sentences = "Negotiations among the senators have intensified significantly in recent days as they push toward a goal of announcing comprehensive immigration legislation in early April. Senators from both parties and their staffs met for hours on Thursday as they struggled to overcome obstacles that several people familiar with the negotiations said could hinder a deal in the weeks ahead."
        tagged_sents = pos.tag(sentences)
        t = parser.build_trees(tagged_sents)
        print "T IS:", t
        assert False
        
        
if __name__ == '__main__':
    unittest.main()