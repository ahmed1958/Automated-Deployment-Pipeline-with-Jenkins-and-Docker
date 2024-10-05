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
        os.environ['REDIS_HOST'] = 'database'
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
        os.environ['REDIS_HOST'] = 'database'
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
            host='database',
            port=6379,
            db=0
        )
        mock_redis_instance.set.assert_called_once_with("counter", 0)

    @patch('redis.Redis')
    def test_redis_connection_failure(self, mock_redis):
        mock_redis.side_effect = redis.exceptions.ConnectionError

        # Set environment variables
        os.environ['REDIS_HOST'] = 'database'
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
    