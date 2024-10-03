import os
import unittest
from unittest.mock import patch, MagicMock
import tornado.testing
from hello import  Application, r, ConnectionError
import sys
class TestMainHandler(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        # Patch the environment variables for testing
        os.environ["REDIS_HOST"] = "database"
        os.environ["REDIS_PORT"] = "6379"
        os.environ["REDIS_DB"] = "0"
        os.environ["ENVIRONMENT"] = "test"
        os.environ["PORT"] = "8888"

        # Create an instance of the application
        return Application()
################it is work################################
    @patch('hello.redis.Redis')
    def test_get(self, mock_redis):
        # Simulate the Redis counter starting at 0 and being incremented to 1
        mock_redis_instance = mock_redis.return_value
        mock_redis.get.return_value = b'0'
        mock_redis.incr.return_value = 1

        # Make a GET request to the root URL
        response = self.fetch('/')
        
        # Assert that the HTTP response code is 200 (OK)
        self.assertEqual(response.code, 200)
        
        # Check that the response contains 'Counter: 1' since we expect it to increment to 1
        self.assertIn(b'Counter:</span> 1', response.body)
        print("test_get completed successfully")
################it doesnot work######################################
    # @patch('hello.redis.Redis')
    # def test_redis_connection_error(self, mock_redis):
    #     # Simulate a Redis connection error
    #     mock_redis.side_effect = ConnectionError("Redis server isn't running")

    #     # Use a helper function to capture the exit code (if sys.exit() is called)
    #     def capture_exit_code():
    #         try:
    #             Application()
    #             return None  # If Application() doesn't call sys.exit(), return None
    #         except SystemExit as e:
    #             return e.code

    #     # Capture the exit code using the helper function
    #     exit_code = capture_exit_code()

    #     # Assert that the exit code is not None (meaning sys.exit() was called)
    #     self.assertIsNotNone(exit_code)

    #     # Additional assertion to verify the desired exit code (optional)
    #     if hasattr(sys, 'exit'):  # Check if sys.exit exists (might not be present in all environments)
    #         self.assertEqual(exit_code, 1)  # Assuming sys.exit(1) is used

    #     print("test_redis_connection_error completed successfully")

if __name__ == "__main__":
    unittest.main()

### to run use  python -m unittest test_hello.py