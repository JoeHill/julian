import unittest
import sys, os

from __init__ import TestApi

from django.utils.timezone import now

from discourse.api import note

class NoteTest(TestApi):
    def test_exists(self):
        n, created = self.get_note()
        self.assertTrue(note.exists(n.identifier))
    
    def test_find_by_id(self):
        n, created = self.get_note()
        target, errors = note.find_by_id(n.id)
        self.assertEquals(n.id, target.id)
        self.assertEquals(n.identifier, u'http://www.google.com/')
        self.assertTrue(not errors)
    
if __name__ == '__main__':
    unittest.main()