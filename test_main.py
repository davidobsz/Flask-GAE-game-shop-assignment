import unittest
import unittest
from main import app, deleteItems


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

            # data that will be used to log in
            data = {
                'name': 'Test@email.com',
                'review': 'test'
            }

            # Make a POST request to the /login route with the data
            response = self.app.post('/login', data=data)

            # Check logging in doesn't break the page
            # Check if the response has a 200 status code (indicating success)
            self.assertEqual(response.status_code, 200)

    # Test adding products to the stock
    def test_adding_item_to_stock(self):
        with app.test_request_context():
            data = {
                "name": "test",
                "price": "test",
                "bluetooth": "test",
                "img": "test",
                "cpu": "test",
                "releaseDate": "test",
                "storage": "test",
                "ram": "test",
                "stock": "test",
                "gpu": "test"
            }

            # Make a POST request to the /add_items route with the data
            response = self.app.post('/add_items', data=data)

            # Check if the response has a 200 status code (indicating success)
            self.assertEqual(response.status_code, 200)

    # This tests the function of deleting a product from the stock
    def test_deleting_item_from_stock(self):
        with app.test_request_context():
            data = {
                "item": "test"
            }

            # Make a POST request to the /delete_items route with the data
            response = self.app.post('/delete_items', data=data)

            # Check if the response has a 200 status code (indicating success)
            self.assertEqual(response.status_code, 200)


    # Checks if the update of stock function works in /admin route
    def test_updating_stock_amount(self):
        with app.test_request_context():
            data = {
                "item": "5",
                "itemName": "PS5"
            }

            # Make a POST request to the /admin route with the data
            # This should change the PS5 Stock number to 3
            response = self.app.post('/admin', data=data)

            # Check if the response has a 200 status code (indicating success)
            self.assertEqual(response.status_code, 200)



    # This test if passed shows that all is OK with the write-reviews page.
    def test_write_comments_page(self):
        with app.test_request_context():
            # Make a POST request to the /comments route with the data
            response = self.app.get('/write-reviews')

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
