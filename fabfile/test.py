import os
from subprocess import call

from fabric.api import task
from fabric.operations import *
from fabric.context_managers import lcd

from fabfile import ROOT

DATABASES_READY = False

@task
def setup_test_database():
	global DATABASES_READY
	if DATABASES_READY:
		return DATABASES_READY
	# Set up test settings (database)
	os.environ['DJANGO_SETTINGS_MODULE'] = 'julian.test_settings'
	pp = []
	if 'PYTHONPATH' in os.environ:
		pp = os.environ['PYTHONPATH'].split( ':' )
	pp.append( ROOT )
	pp.append( ROOT.replace( 'julian', '' ) )
	os.environ['PYTHONPATH'] = ":".join( pp )
	# Run migrations
	with lcd(ROOT):
		# Drop tables
		call( " ".join( [ 'python', 'manage.py', 'syncdb' ] ), shell=True )
		call( " ".join( [ 'python', 'manage.py', 'migrate', 'discourse' ] ) , shell=True )
		DATABASES_READY = True
	return DATABASES_READY		

@task
def discourse():
	"""Run discourse tests."""
	if setup_test_database():
		test_path = ROOT + '/discourse/tests/'
		test_filenames = os.listdir(test_path)
		paths = [ test_path + f for f in test_filenames ]
		with lcd(ROOT):
			for p in paths:
				call( " ".join( [ 'python', p ] ) )
				
@task
def node():
	"""Run node tests"""
	if setup_test_database():
		with lcd(ROOT):
			call( " ".join( ['python', 'discourse/tests/node_test.py'] ), shell=True )

@task
def edge():
	"""Run edge tests"""
	if setup_test_database():
		with lcd(ROOT):
			call( " ".join( ['python', 'discourse/tests/edge_test.py'] ), shell=True )		
			
@task
def note():
	"""Run note tests"""
	if setup_test_database():
		with lcd(ROOT):
			call( " ".join( ['python', 'discourse/tests/note_test.py'] ), shell=True )

@task
def inference():
	"""Run interence tests"""
	if setup_test_database():
		with lcd(ROOT):
			call( " ".join( ['python', 'discourse/tests/inference_test.py'] ), shell=True )
