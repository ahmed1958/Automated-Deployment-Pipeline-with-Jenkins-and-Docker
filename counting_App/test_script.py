import os
import unittest
import redis
import tornado.ioloop
import tornado.httpclient
from tornado.testing import AsyncHTTPTestCase, gen_test
from hello import Application  # Import your existing Application class

class TestRedisFunctionality(AsyncHTTPTestCase):

    def get_app(self):
        # Patch the environment variables for testing
        os.environ["REDIS_HOST"] = "database"
        os.environ["REDIS_PORT"] = "6379"
        os.environ["REDIS_DB"] = "0"
        os.environ["ENVIRONMENT"] = "test"
        os.environ["PORT"] = "8888"

        # Create an instance of the application
        return Application()

    def setUp(self):
        super().setUp()  # Call the parent setUp method
        # Initialize Redis connection
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB"))
        )
        # Ensure Redis is empty before tests
        self.redis_client.flushdb()

    def tearDown(self):
        # Clean up Redis after each test
        self.redis_client.flushdb()

    @gen_test  # Decorate with @gen_test to manage async tests
    async def test_redis_connection(self):
        # Test if Redis is connected by setting and getting a value
        self.redis_client.set('test_key', 'test_value')
        value = self.redis_client.get('test_key').decode('utf-8')
        self.assertEqual(value, 'test_value', "Redis should return the correct value")

    @gen_test  # Decorate with @gen_test to manage async tests
    async def test_button_click(self):
        # Simulate a button click on the local web app
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(self.get_url('/click'), method='POST', body='')  # Added empty body
        self.assertEqual(response.code, 200, "The button click should return 200 status")

        # Check if Redis stored the click count
        click_count = int(self.redis_client.get('counter').decode('utf-8'))
        self.assertEqual(click_count, 1, "Redis should store one click count")

    @gen_test  # Decorate with @gen_test to manage async tests
    async def test_multiple_clicks(self):
        # Simulate multiple clicks
        http_client = tornado.httpclient.AsyncHTTPClient()
        for _ in range(5):
            await http_client.fetch(self.get_url('/click'), method='POST', body='')  # Added empty body

        # Check if Redis stored the correct number of clicks
        click_count = int(self.redis_client.get('counter').decode('utf-8'))
        self.assertEqual(click_count, 5, "Redis should store five clicks")

if __name__ == '__main__':
    unittest.main()

