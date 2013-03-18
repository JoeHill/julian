import unittest

from discourse.models import Node, Edge, Note
from discourse.api import node

from utils import print_errors_and_exit

class TestNode(unittest.TestCase):
    
    def create_note(self):
        self.n = Note.objects.create( identifier=u'test_note',
                                 prioritya=u"Obama Sketches a Firmly Progressive Agenda.",
                                 priorityb=u"""Mr. Obama went out of his way to mention both gay rights and the need to address climate change in a speech that seemed intended to assert his authority over his political rivals and to define his version of modern liberalism after voters returned him to office for a second term.""" )
    
        self.s = self.n.prioritya + u' ' + self.n.priorityb
    
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
    
    
    def test_get_from_note_id_and_get_from_string(self):
        ns, errors = node.get_from_note_id(self.n.id)
        print_errors_and_exit( errors )
        ms, errors = node.get_from_string( self.n.prioritya + u" " + self.n.priorityb )
        print_errors_and_exit( errors )


        actual = [ m.title for m in ms ]
        expected = [ n.title for n in ns ]
        
        actual.sort()
        expected.sort()
        
        assert 0 < len( actual )
        assert 0 < len( expected )
        assert len( actual ) == len( expected )
        
        checks = zip( actual, expected )

        for check in checks:
            assert check[0] == check[1]


    def test_create_from_note_id(self):
        expected_nodes, errors = node.get_from_note_id(self.n.id)
        print_errors_and_exit( errors )

            
        actual_nodes, errors = node.create_from_note_id(self.n.id)
        print_errors_and_exit( errors )

            
        expected_titles = [ n.title for n in expected_nodes ]
        actual_titles = [ n.title for n in actual_nodes ]
        
        assert len( expected_titles ) > 0
        assert len( actual_titles ) > 0
        assert len( expected_titles ) == len( actual_titles )
        
        expected_titles.sort()
        actual_titles.sort()
        
        expected_actual = zip( expected_titles, actual_titles )
        for exp, act in expected_actual:
            assert exp == act
            

    def test_get_or_create_by_title_and_note_id(self):
        title = 'test_title'
        ( n, created ), errors = node.get_or_create_by_title_and_note_id(title, self.n.id)
        print_errors_and_exit( errors )
            
        assert n.title == title
        assert created
        
        ( n, created ), errors = node.get_or_create_by_title_and_note_id(title, self.n.id)
        print_errors_and_exit( errors )
            
        assert n.title == title
        assert not created

        
    def find_stored_by_note_id(self): # TODO: finish this test. Build edges and find nodes by note id
        expected_nodes, errors = node.get_from_note_id(self.n.id)
        print_errors_and_exit( errors )

            
        actual_nodes, errors = node.create_from_note_id(self.n.id)
        print_errors_and_exit( errors )

        
        expected_titles = [ n.title for n in expected_nodes ]
        actual_titles = [ n.title for n in actual_nodes ]
        
        assert len( expected_titles ) > 0
        assert len( actual_titles ) > 0
        assert len( expected_titles ) == len( actual_titles )
        
        expected_titles.sort()
        actual_titles.sort()
        
        expected_actual = zip( expected_titles, actual_titles )
        for exp, act in expected_actual:
            assert exp == act

    
    def test_find_by_ids(self):
        expected_nodes, errors = node.get_from_note_id(self.n.id)
        print_errors_and_exit( errors )
            
        actual_nodes, errors = node.create_from_note_id(self.n.id)
        print_errors_and_exit( errors )
        
        expected_titles = [ n.title for n in expected_nodes ]
        actual_titles = [ n.title for n in actual_nodes ]
        
        assert len( expected_titles ) > 0
        assert len( actual_titles ) > 0
        assert len( expected_titles ) == len( actual_titles )
        
        expected_titles.sort()
        actual_titles.sort()
        
        expected_actual = zip( expected_titles, actual_titles )
        for exp, act in expected_actual:
            assert exp == act
            
        ids = [ n.id for n in actual_nodes ]
        nodes, errors = node.find_by_ids( ids )
        fetched_ids = [ n.id for n in nodes ]
        
        ids.sort()
        fetched_ids.sort()
        
        assert len( ids ) > 0 
        assert len( fetched_ids ) > 0
        assert len( ids ) == len( fetched_ids )
        
        checks = zip( ids, fetched_ids )
        for exp, act in checks:
            assert exp == act
            
if __name__ == '__main__':
    unittest.main()