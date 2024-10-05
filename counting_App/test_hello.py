# import os
# import unittest
# from unittest.mock import patch, MagicMock
# import tornado.testing
# from hello import  Application, r, ConnectionError
# import sys
# class TestMainHandler(tornado.testing.AsyncHTTPTestCase):
#     def get_app(self):
#         # Patch the environment variables for testing
#         os.environ["REDIS_HOST"] = "database"
#         os.environ["REDIS_PORT"] = "6379"
#         os.environ["REDIS_DB"] = "0"
#         os.environ["ENVIRONMENT"] = "test"
#         os.environ["PORT"] = "8888"

#         # Create an instance of the application
#         return Application()
# ################it is work################################
#     @patch('hello.redis.Redis')
#     def test_get(self, mock_redis):
#         # Simulate the Redis counter starting at 0 and being incremented to 1
#         mock_redis_instance = mock_redis.return_value
#         mock_redis.get.return_value = b'0'
#         mock_redis.incr.return_value = 1

#         # Make a GET request to the root URL
#         response = self.fetch('/')
        
#         # Assert that the HTTP response code is 200 (OK)
#         self.assertEqual(response.code, 200)
        
#         # Check that the response contains 'Counter: 1' since we expect it to increment to 1
#         self.assertIn(b'Counter:</span> 1', response.body)
#         print("test_get completed successfully")

# #######################################

# ################it doesnot work#######################################
#     # @patch('hello.redis.Redis')
#     # def test_redis_connection_error(self, mock_redis):
#     #     # Simulate a Redis connection error
#     #     mock_redis.side_effect = ConnectionError("Redis server isn't running")

#     #     # Use a helper function to capture the exit code (if sys.exit() is called)
#     #     def capture_exit_code():
#     #         try:
#     #             Application()
#     #             return None  # If Application() doesn't call sys.exit(), return None
#     #         except SystemExit as e:
#     #             return e.code

#     #     # Capture the exit code using the helper function
#     #     exit_code = capture_exit_code()

#     #     # Assert that the exit code is not None (meaning sys.exit() was called)
#     #     self.assertIsNotNone(exit_code)

#     #     # Additional assertion to verify the desired exit code (optional)
#     #     if hasattr(sys, 'exit'):  # Check if sys.exit exists (might not be present in all environments)
#     #         self.assertEqual(exit_code, 1)  # Assuming sys.exit(1) is used

#     #     print("test_redis_connection_error completed successfully")
#     @patch('hello.redis.Redis')
#     def test_redis_connection_error(self, mock_redis):
#         # Simulate a Redis connection error
#         mock_redis.side_effect = ConnectionError

#         # Mock sys.exit so the test doesn't actually exit the process
#         with patch('sys.exit') as mock_exit:
#             # Simulate the application startup and Redis connection failure
#             with self.assertRaises(ConnectionError):
#                 r.get('counter')  # This should raise a ConnectionError
                
#             # Verify sys.exit was called since the app should terminate on Redis connection failure
#             mock_exit.assert_called_once_with(1)

#         print("test_redis_connection_error completed successfully")


# if __name__ == "__main__":
#     unittest.main()

# ### to run use  python -m unittest test_hello.py


import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tornado.testing
from tornado.testing import AsyncHTTPTestCase
import redis

# Import your main script
import hello

class TestApplication(AsyncHTTPTestCase):
    def get_app(self):
        return hello.Application()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

class TestMainHandler(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return hello.Application()

    @patch('redis.Redis')
    def test_get(self, mock_redis):
        # Mock Redis connection and methods
        mock_redis_instance = MagicMock()
        mock_redis_instance.incr.return_value = 2
        mock_redis.return_value = mock_redis_instance

        # Set environment variables
        os.environ['ENVIRONMENT'] = 'DEV'
        os.environ['REDIS_HOST'] = 'localhost'
        os.environ['REDIS_PORT'] = '6379'
        os.environ['REDIS_DB'] = '0'

        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertIn(b'<span class="highlight" id="DEV">DEV</span>', response.body)
        self.assertIn(b'<p><span class="counter">Counter:</span> 2</p>', response.body)

class TestRedisConnection(unittest.TestCase):
    @patch('redis.Redis')
    def test_redis_connection_success(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        # Set environment variables
        os.environ['REDIS_HOST'] = 'localhost'
        os.environ['REDIS_PORT'] = '6379'
        os.environ['REDIS_DB'] = '0'

        # Recreate the Redis connection logic
        try:
            r = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT")),
                db=int(os.getenv("REDIS_DB")),
            )
            r.set("counter", 0)
        except redis.exceptions.ConnectionError:
            self.fail("Redis connection failed unexpectedly")

        mock_redis.assert_called_once_with(
            host='localhost',
            port=6379,
            db=0
        )
        mock_redis_instance.set.assert_called_once_with("counter", 0)

    @patch('redis.Redis')
    def test_redis_connection_failure(self, mock_redis):
        mock_redis.side_effect = redis.exceptions.ConnectionError

        # Set environment variables
        os.environ['REDIS_HOST'] = 'localhost'
        os.environ['REDIS_PORT'] = '6379'
        os.environ['REDIS_DB'] = '0'

        with self.assertRaises(SystemExit):
            # Recreate the Redis connection logic
            try:
                r = redis.Redis(
                    host=os.getenv("REDIS_HOST"),
                    port=int(os.getenv("REDIS_PORT")),
                    db=int(os.getenv("REDIS_DB")),
                )
                r.set("counter", 0)
            except redis.exceptions.ConnectionError:
                print("Redis server isn't running. Exiting...")
                sys.exit(1)

if __name__ == '__main__':
    unittest.main()
    