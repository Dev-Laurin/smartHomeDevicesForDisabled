import os 
import tempfile

import pytest

from smartify import smartify 

@pytest.fixture
def client():
	db_fd, smartify.app.config['DATABASE'] = tempfile.mkstemp()
	smartify.app.config['TESTING'] = True 

	with smartify.app.test_client() as client: 
		with smartify.app.app_context():
			smartify.init_db()
		yield client 

	os.close(db_fd)
	os.unlink(smartify.app.config['DATABASE'])