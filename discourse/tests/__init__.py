import sys, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path = [ROOT] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

from django.test import TransactionTestCase
from django.utils.timezone import now

from discourse.api import note

class TestApi(TransactionTestCase):
    
    def get_note(self):
        (n, created), errors = note.get_or_create( identifier='http://www.google.com/', 
                                               prioritya="The quick brown fox jumped over the lazy dog.", 
                                               priorityb="Lorem ipsum dolor sit.", 
                                               priorityc="The knights who say ni.", 
                                               priorityd="", 
                                               prioritye="", 
                                               published_at=now() )

        return n, created