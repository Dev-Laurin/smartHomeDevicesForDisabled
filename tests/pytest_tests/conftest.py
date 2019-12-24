import os 
import pytest

from smartify import create_app 
from smartify import db as _db 

@pytest.fixture(scope='session')
def app(request):
	"""Session-wide Flask application."""
	app = create_app(dev_config=True)

	testing_client = app.test_client() 

	#Establish an application context before running the tests. 
	ctx = app.app_context() 
	ctx.push() 

	yield testing_client 

	ctx.pop()

@pytest.fixture(scope='session')
def db(app, request):
	"""Session-wide test database."""
	_db.app = app 
	_db.create_all() 

	yield _db 

	_db.drop_all()  

@pytest.fixture(scope='function')
def session(db, request):
	"""Creates a new database session for a test."""
	connection = db.engine.connect() 
	transaction = connection.begin() 

	options = dict(bind=connection, binds={})
	session = db.create_scoped_session(options=options)

	db.session = session 

	def teardown():
		transaction.rollback() 
		connection.close()
		session.remove() 

	request.addfinalizer(teardown)
	return session 

