import os
import flaskengine
import unittest
import mongoengine
from flaskengine import settings

class FlaskrTestCase(unittest.TestCase):
    
    def setUp(self):
        settings.DATABASE = 'flaskengine_test'
        self.app = flaskengine.app.test_client()
        self.db = flaskengine.connect_db()
    
    def tearDown(self):
        self.db.connection.drop_database(settings.DATABASE)
    
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
    
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    def test_empty_db(self):
        response = self.app.get('/')
        assert 'No entries so far' in response.data
    
    def test_login_logout(self):
        response = self.login(settings.USERNAME, settings.PASSWORD)
        assert 'You have been logged in' in response.data
        response = self.logout()
        assert 'You have been logged out' in response.data
        response = self.login(settings.USERNAME + 'X', settings.PASSWORD)
        assert 'Invalid username' in response.data
        response = self.login(settings.USERNAME, settings.PASSWORD + 'X')
        assert 'Invalid password' in response.data
    
    def test_messages(self):
        self.login(settings.USERNAME, settings.PASSWORD)
        response = self.app.post('/add', data=dict(
            title='<Hello>',
            text='**HTML** allowed here'
        ), follow_redirects=True)
        assert 'No entries so far' not in response.data
        assert '&lt;Hello&gt;' in response.data
        assert '<strong>HTML</strong> allowed here' in response.data


suite = unittest.TestLoader().loadTestsFromTestCase(FlaskrTestCase)


if __name__ == '__main__':
    unittest.main()