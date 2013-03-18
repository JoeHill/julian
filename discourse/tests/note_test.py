import unittest

from julian.discourse.api import note

class NoteTest(unittest.TestCase):
    def test_exists(self):
        self.assertTrue(note.exists(u'http://money.msn.com/investing/would-a-us-default-mean-disaster-jubak.aspx'))
    
    def test_find_by_id(self):
        n, errors = note.find_by_id(3022)
        self.assertEquals(n.id, 3022)
        self.assertEquals(n.identifier, u'http://money.msn.com/investing/would-a-us-default-mean-disaster-jubak.aspx')
        self.assertTrue(not errors)
        
    def test_get_or_create(self):
        pass
    
    def test_find_all(self):
        ns, errors = note.find_all()
        self.assertTrue( not errors )
        
    
if __name__ == '__main__':
    unittest.main()