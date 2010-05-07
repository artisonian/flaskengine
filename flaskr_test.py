import os
import flaskr
import unittest
import mongoengine

class FlaskrTestCase(unittest.TestCase):
    
    def setUp(self):
        flaskr.DATABASE = 'flaskengine_test'
        self.app = flaskr.app.test_client()
        self.db = flaskr.connect_db()
    
    def tearDown(self):
        self.db.connection.drop_database(flaskr.DATABASE)
    
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
        response = self.login(flaskr.USERNAME, flaskr.PASSWORD)
        assert 'You have been logged in' in response.data
        response = self.logout()
        assert 'You have been logged out' in response.data
        response = self.login(flaskr.USERNAME + 'X', flaskr.PASSWORD)
        assert 'Invalid username' in response.data
        response = self.login(flaskr.USERNAME, flaskr.PASSWORD + 'X')
        assert 'Invalid password' in response.data
    
    def test_messages(self):
        self.login(flaskr.USERNAME, flaskr.PASSWORD)
        response = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries so far' not in response.data
        assert '&lt;Hello&gt;' in response.data
        assert '<strong>HTML</strong> allowed here' in response.data


if __name__ == '__main__':
    unittest.main()