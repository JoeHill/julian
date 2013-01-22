import unittest
import os

from julian.discourse.models import Node, Edge, Note
from julian.discourse.api import node

class TestNode(unittest.TestCase):
    
    def create_note(self):
        self.n = Note.objects.create( identifier=u'test_note',
                                 prioritya=u"Obama Sketches a Firmly Progressive Agenda",
                                 priorityb=u"""Mr. Obama went out of his way to mention both gay rights and the need to address climate change in a speech that seemed intended to assert his authority over his political rivals and to define his version of modern liberalism after voters returned him to office for a second term.""" )
    
    def setUp(self):
        self.create_note()
        
    def tearDown(self):
        nodes = Node.objects.all()
        for n in nodes:
            n.delete()
        edges = Edge.objects.all()
        for e in edges:
            e.delete()
        notes = Note.objects.all()
        for n in notes:
            n.delete() 
    
    def test_get_from_note_id(self):
        ns, errors = node.get_from_note_id(self.n.id)
        if errors:
            print errors
            assert False

        ms, errors = node.get_from_string( self.n.prioritya + u" " + self.n.priorityb )
        if errors:
            print errors
            assert False

        actual = [ m.title for m in ms ]
        expected = [ n.title for n in ns ]
        
        actual.sort()
        expected.sort()
            
        checks = zip( actual, expected )

        for check in checks:
            print u'>>' + unicode( check[0] ) + " == " + unicode( check[1] ) + u'<<'
            assert check[0] == check[1]

    def test_create_from_note_id(self):
        expected_nodes, errors = node.get_from_note_id(self.n.id)
        actual_nodes, errors = node.create_from_note_id(self.n.id)
        
        expected_titles = [ n.title for n in expected_nodes ]
        actual_titles = [ n.title for n in actual_nodes ]
        
        expected_titles.sort()
        actual_titles.sort()
        
        expected_actual = zip( expected_titles, actual_titles )
        for exp, act in expected_actual:
            assert exp == act
    
    def test_find_by_ids(self):
        pass
    
if __name__ == '__main__':
    unittest.main()