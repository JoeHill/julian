import unittest

from nltk.draw.tree import draw_trees

import sys

from discourse.services.nltk import pos
from discourse.services.collins import parser

class TestCollinsParser(unittest.TestCase):
    
    def test_collins_to_tree(self):
        s = """(TOP~confirmed~1~1 (S~confirmed~2~2 (NPB~Korea~2~2 North/NNP Korea/NNP ) (VP~confirmed~4~1 confirmed/VBD (PP~on~2~1 on/IN (NPB~Tuesday~1~1 Tuesday/NNP ) ) (SBAR-A~that~2~1 that/IN (S-A~had~2~2 (NPB~it~1~1 it/PRP ) (VP~had~3~1 had/VBD (VP-A~conducted~2~1 conducted/VBN (NPB~test~5~5 its/PRP$ third/JJ ,/PUNC, long-threatened/NN nuclear/JJ test/NN ,/PUNC, ) ) (PP~according~2~1 according/VBG (PP-A~to~2~1 to/TO (NPB~service~5~5 the/DT official/JJ KCNA/NN news/NN service/NN ,/PUNC, ) ) ) ) ) ) (SG~posing~1~1 (VP~posing~3~1 posing/VBG (NP-A~challenge~2~1 (NPB~challenge~3~3 a/DT new/JJ challenge/NN ) (PP~for~2~1 for/IN (NPB~administration~3~3 the/DT Obama/NN administration/NN ) ) ) (PP~in~2~1 in/IN (NP-A~effort~2~1 (NPB~effort~2~2 its/PRP$ effort/NN ) (SG~to~1~1 (VP~to~2~1 to/TO (VP-A~keep~3~1 keep/VB (NPB~country~2~2 the/DT country/NN ) (PP~from~2~1 from/IN (SG-A~becoming~1~1 (VP~becoming~2~1 becoming/VBG (NPB~power~4~4 a/DT full-fledged/JJ nuclear/JJ power/NN ./PUNC. ) ) ) ) ) ) ) ) ) ) ) ) ) )"""
        sys.stderr.write( s + '\n')
        tree = parser.collins_to_tree(s)
        draw_trees(tree)
        assert False

    """
    def test_pos_tagged_to_collins_tree(self):
        sentences = "North Korea confirmed on Tuesday that it had conducted its third, long-threatened nuclear test, according to the official KCNA news service, posing a new challenge for the Obama administration in its effort to keep the country from becoming a full-fledged nuclear power."
        tagged_sents = pos.tag(sentences)
        t = parser.build_trees(tagged_sents)
        assert False
    """
        
if __name__ == '__main__':
    unittest.main()
