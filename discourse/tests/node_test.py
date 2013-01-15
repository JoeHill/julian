import unittest

from julian.discourse.api import node

class TestNode(unittest.TestCase):
    
    def test_get_or_create_from_note_id(self):
        ns, errors = node.get_or_create_from_note_id(3022)
        for err in errors:
            print err
            
        for n in ns:
            print n.title
            
        assert False
    
    def test_find_by_note_id(self):
        pass
    
    def test_find_by_ids(self):
        pass
    
if __name__ == '__main__':
    unittest.main()