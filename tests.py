import unittest
from flask_testing import TestCase
from app import app

class MyAppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_admin_route(self):
        # Test the /admin route
        response = self.client.get('/admin')
        self.assert200(response)  # Verify that the response has a status code of 200
        self.assert_template_used('admin_login.html')  # Verify that the correct template is used

    def test_adminlogin_validation_correct_credentials(self):
        # Test the /adminlogin_validation route with correct credentials
        response = self.client.post('/adminlogin_validation', data=dict(email='admin123@gmail.com', password='admin'))
        self.assert200(response)
        self.assert_template_used('Admin.html')

    def test_adminlogin_validation_incorrect_credentials(self):
    # Test the /adminlogin_validation route with incorrect credentials
        response = self.client.post('/adminlogin_validation', data=dict(email='admin456@gmail.com', password='wrongpassword'))
        self.assert200(response)
        self.assert_context('response', 'Check ur credentials')


    def test_adminpanel_authenticated(self):
        # Test the /adminpanel route when the user is authenticated
        with self.client:
            self.client.post('/adminlogin_validation', data=dict(email='admin123@gmail.com', password='admin'))
            response = self.client.get('/adminpanel')
            self.assert200(response)
            self.assert_template_used('Admin.html')

    def test_adminpanel_unauthenticated(self):
    # Test the /adminpanel route when the user is not authenticated
        response = self.client.get('/adminpanel', follow_redirects=False)
        self.assertStatus(response, 302)  # Verify that the response has a status code of 302 (redirect)
        self.assertEqual(response.location, '/admin')  # Verify that the response is redirected to /admin


    def test_logout_admin(self):
        # Test the /logoutadmin route
        response = self.client.get('/logoutadmin', follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('viewword.html')

if __name__ == '__main__':
    unittest.main()
