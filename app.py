import signal
import logging
import logging.config

import tornado.web
import tornado.gen
import tornado.ioloop
from tornado.httpserver import HTTPServer
from envparse import env

from utils.db import Database

logging.config.fileConfig('logging.conf')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        sql = "SELECT table_name FROM information_schema.tables;"
        res = await app.db.query(sql)
        print(res)
        self.write("Hello world")
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        self._set_env_config()

        logger.debug('Create DB connection pool')
        self.db = Database(
            host=self.MYSQL_HOST,
            port=self.MYSQL_HOST,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            database=self.MYSQL_DATABASE
        )
        # TODO: get handlers from apps
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            debug=self.DEBUG
        )
        super().__init__(handlers=handlers, **settings)

    def _set_env_config(self):
        """
        Read .env file and set configs to be accessed from app.
        """
        logger.debug('Set env config')
        self.DEBUG = env.bool('DEBUG')
        self.APP_PORT = env.bool('APP_PORT')
        self.MYSQL_HOST = env('MYSQL_HOST')
        self.MYSQL_PORT = env('MYSQL_PORT')
        self.MYSQL_DATABASE = env('MYSQL_DATABASE')
        self.MYSQL_USER = env('MYSQL_USER')
        self.MYSQL_PASSWORD = env('MYSQL_PASSWORD')
        self.SHUTDOWN_WAIT_TIME = env('SHUTDOWN_WAIT_TIME')

    async def _shutdown(self):
        """
        Graceful shutdown. Stops receiving new requests, wait SHUTDOWN_WAIT_TIME to give chance to process existing
        requests, stop ioloop and close DB connection.
        """
        logger.debug('Shutdown stop server')
        server.stop()

        # in real app could be extended to request endpoint for check active requests count
        logger.debug(f'Shutdown waiting {self.SHUTDOWN_WAIT_TIME} seconds to process existing requests')
        await tornado.gen.sleep(self.SHUTDOWN_WAIT_TIME)
        tornado.ioloop.IOLoop.current().stop()

        logger.debug('Shutdown close pool connection')
        self.db.pool.close()

    def exit_handler(self, sig, frame):
        """
        Add callback handler for graceful shutdown on signal received.
        """
        logger.debug(f'Shutdown signal received {sig}')
        tornado.ioloop.IOLoop.current().add_callback_from_signal(self._shutdown)


if __name__ == "__main__":
    logger.debug('Start application')
    app = Application()
    server = HTTPServer(app)

    signal.signal(signal.SIGQUIT, app.exit_handler)
    signal.signal(signal.SIGTERM, app.exit_handler)
    signal.signal(signal.SIGINT, app.exit_handler)

    server.listen(app.APP_PORT)
    logger.debug(f'Listening on port {app.APP_PORT}')
    tornado.ioloop.IOLoop.current().start()
