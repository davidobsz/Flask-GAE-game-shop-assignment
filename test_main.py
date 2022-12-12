import unittest
import unittest
from main import app


class TestApp(unittest.TestCase):

   # set the app that it is running
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    # test that /home response with status code 200 (OK)
    def test_app_is_online(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(response.data)


    # Test posting a comment
    def test_post_comment(self):
        with app.test_request_context():
            # Set the data to be sent with the POST request
            data = {
                'name': 'Test User',
                'review': 'This is a test review'
            }

            # Make a POST request to the /comments route with the data
            response = self.app.post('/comments', data=data)

            # Check if the response has a 200 status code (indicating success)
            self.assertEqual(response.status_code, 200)


    # Test the login page returns 200 status code (success)
    def test_login_page(self):
        with app.test_request_context():
            response = self.app.get('/login')


            data = {
                'name': 'Test User',
                'review': 'This is a test review'
            }

            # Make a POST request to the /login route with the data
            response = self.app.post('/login', data=data)


            # Check logging in doesnt break the page
            # Check if the response has a 200 status code (indicating success)
            self.assertEqual(response.status_code, 200)



    # Test getting shop items
    def test_getting_shop_items(self):
        with app.test_request_context():

            # Make a GET request to the /comments route with the data
            response = self.app.get('/shop')

            # Check if the response has a 200 status code (indicating success)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

