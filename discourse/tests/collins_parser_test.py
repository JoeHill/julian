import unittest

import sys

from discourse.services.collins import parser as collins_parser

class TestCollinsParser(unittest.TestCase):
    
    def test_pos_tagged_to_collins_tree(self):
        sys.stderr.write( "This test has not yet been implemented\n" )
        assert False