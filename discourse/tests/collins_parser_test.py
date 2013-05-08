import unittest

from nltk.draw.tree import draw_trees

import sys

from discourse.services.nltk import pos
from discourse.services.collins import parser

class TestCollinsParser(unittest.TestCase):

    def test_collins_to_tree(self):
        """
        s = "(TOP~is~1~1 (S~is~2~2 (NP-A~brother~2~1 (NPB~brother~2~2 My/PRP$ brother/NN ,/PUNC, ) (NP~Adam~2~1 Adam/NP ,/PUNC, (SBAR~who~2~1 (WHNP~who~1~1 who/WP ) (SG-A~finished~2~2 (ADVP~just~1~1 just/RB ) (VP~finished~2~1 finished/VBD (NPB~dissertation~2~2 his/PRP$ dissertation/NN ,/PUNC, ) ) ) ) ) ) (VP~is~2~1 is/VBZ (VP-A~headed~2~1 headed/VBN (PP~to~2~1 to/TO (NP-A~Rock~2~1 (NPB~Rock~2~2 Red/NNP Rock/NNP ,/PUNC, ) (NP~Carolina~2~1 (NPB~Carolina~2~2 South/NNP Carolina/NNP ) (NPB~weekend~2~2 this/DT weekend/NN ./PUNC. ) ) ) ) ) ) ) ) "
        """
        s = """
        (TOP~met~1~1 
            (S~met~2~2 
                (NP-A~Senators~3~1 
                    (NP~Senators~2~1 
                        (NPB~Senators~1~1 Senators/NNS ) 
                        (PP~from~2~1 from/IN 
                            (NPB~parties~2~2 both/DT parties/NNS ) 
                        ) 
                    ) 
                    and/CC 
                    (NPB~staffs~2~2 their/PRP$ staffs/NNS ) 
                ) 
                (VP~met~4~1 met/VBD 
                    (PP~for~2~1 for/IN 
                        (NPB~hours~1~1 hours/NNS ) 
                    ) 
                    (PP~on~2~1 on/IN 
                        (NPB~Thursday~1~1 Thursday/NNP ) 
                    ) 
                    (SBAR~as~2~1 as/IN 
                        (S-A~struggled~2~2 
                            (NPB~they~1~1 they/PRP ) 
                            (VP~struggled~4~1 struggled/VBD 
                                (SG-A~to~1~1 
                                    (VP~to~2~1 to/TO 
                                        (VP-A~overcome~2~1 overcome/VB 
                                            (NP-A~obstacles~2~1 
                                                (NPB~obstacles~1~1 obstacles/NNS ) 
                                                (SBAR~that~2~1 that/IN 
                                                    (S-A~could~2~2 
                                                        (NP-A~people~2~1 
                                                            (NPB~people~2~2 several/JJ people/NNS ) 
                                                            (ADJP~familiar~2~1 familiar/JJ 
                                                                (PP~with~2~1 with/IN 
                                                                    (NP-A~negotiations~2~1 
                                                                        (NPB~negotiations~2~2 the/DT negotiations/NNS ) 
                                                                        (VP~said~1~1 said/VBD ) 
                                                                    ) 
                                                                ) 
                                                            ) 
                                                        ) 
                                                        (VP~could~1~1 could/MD ) 
                                                    ) 
                                                ) 
                                            ) 
                                        ) 
                                    ) 
                                ) 
                                (NPB~hinder~1~1 hinder/NN ) 
                                (NP~deal~2~1 
                                    (NPB~deal~2~2 a/DT deal/NN ) 
                                    (PP~in~2~1 in/IN 
                                        (NPB~weeks~3~2 the/DT weeks/NNS ahead/RB ./PUNC. ) 
                                    ) 
                                ) 
                            ) 
                        ) 
                    ) 
                ) 
            ) 
        )
        """
        tree = parser.collins_to_tree(s)
        
    def test_pos_tagged_to_collins_tree(self):
        sentences = "Senators from both parties and their staffs met for hours on Thursday as they struggled to overcome obstacles that several people familiar with the negotiations said could hinder a deal in the weeks ahead."
        tagged_sents = pos.tag(sentences)
        t = parser.build_trees(tagged_sents)        
        
if __name__ == '__main__':
    unittest.main()