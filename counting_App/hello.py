import redis
from redis.exceptions import ConnectionError
import tornado.ioloop
import tornado.web
import logging
import os
import sys

try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        db=int(os.getenv("REDIS_DB")),
    )
    r.set("counter", 0)
except ConnectionError:
    print("Redis server isn't running. Exiting...")
    sys.exit(1)
################################################################
environment = os.getenv("ENVIRONMENT")
port = int(os.getenv("PORT"))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            dict={"environment": environment, "counter": r.incr("counter", 1)},
        )


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = {
            "template_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "templates"
            ),
            "static_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "static"
            ),
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    logging.basicConfig(
    stream=sys.stdout,  # Log to standard output
    level=logging.INFO,  # Set the logging level (INFO in this case)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)
    logger = logging.getLogger(__name__)
    app = Application()
    app.listen(port)
    # logger.info(f"App running: http://{os.getenv('HOST')}:{int(os.getenv('PORT'))}")
    tornado.ioloop.IOLoop.current().start()
