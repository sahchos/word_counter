import os
import signal
import logging
import logging.config

from tornado import web, gen, ioloop
from tornado.httpserver import HTTPServer
from pymysql import ProgrammingError
import jinja2
from envparse import env
from tornado_jinja2 import Jinja2Loader

from utils.db import Database
from word_counter.urls import word_counter_urls

logging.config.fileConfig('logging.conf')
logging.basicConfig(level=logging.DEBUG if env.bool('DEBUG') else logging.INFO)
logger = logging.getLogger(__name__)


class Application(web.Application):
    def __init__(self):
        self._set_env_config()

        logger.debug('Create DB connection pool')
        self.db = Database(
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            database=self.MYSQL_DATABASE
        )

        ioloop.IOLoop.current().add_callback(self._create_tables)

        jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            autoescape=False
        )
        jinja2_loader = Jinja2Loader(jinja2_env)

        settings = dict(
            debug=self.DEBUG,
            template_loader=jinja2_loader
        )
        super().__init__(handlers=self._get_handlers(), **settings)

    def _set_env_config(self):
        """
        Read .env file and set configs to be accessed from app.
        """
        logger.debug('Set env config')
        self.DEBUG = env.bool('DEBUG')
        self.APP_PORT = env.int('APP_PORT')
        self.MYSQL_HOST = env('MYSQL_HOST')
        self.MYSQL_PORT = env.int('MYSQL_PORT')
        self.MYSQL_DATABASE = env('MYSQL_DATABASE')
        self.MYSQL_USER = env('MYSQL_USER')
        self.MYSQL_PASSWORD = env('MYSQL_PASSWORD')
        self.SHUTDOWN_WAIT_TIME = env.int('SHUTDOWN_WAIT_TIME')
        self.PUBLIC_KEY = env('PUBLIC_KEY')
        self.PRIVATE_KEY = env('PRIVATE_KEY')
        self.WORD_SALT = env('WORD_SALT')

    def _get_handlers(self):
        handlers = []
        handlers.extend(word_counter_urls)

        return handlers

    async def _create_tables(self):
        try:
            await self.db.query("SELECT COUNT(*) FROM words LIMIT 1")
        except ProgrammingError:
            await self.db.execute(
                """
                CREATE TABLE `words` (
                    `pk` VARCHAR(255) CHARACTER SET utf8 NOT NULL,
                    `word` VARCHAR(255) CHARACTER SET utf8 NOT NULL,
                    `count` INT NOT NULL,
                    PRIMARY KEY (`pk`,`word`)
                );
                """
            )

    async def _shutdown(self):
        """
        Graceful shutdown. Stops receiving new requests, wait SHUTDOWN_WAIT_TIME to give chance to process existing
        requests, stop ioloop and close DB connection.
        """
        logger.debug('Shutdown stop server')
        server.stop()

        # in real app could be extended to request endpoint for check active requests count
        logger.debug(f'Shutdown waiting {self.SHUTDOWN_WAIT_TIME} seconds to process existing requests')
        await gen.sleep(self.SHUTDOWN_WAIT_TIME)
        ioloop.IOLoop.current().stop()

        logger.debug('Shutdown close pool connection')
        self.db.pool.close()

    def exit_handler(self, sig, frame):
        """
        Add callback handler for graceful shutdown on signal received.
        """
        logger.debug(f'Shutdown signal received {sig}')
        ioloop.IOLoop.current().add_callback_from_signal(self._shutdown)


if __name__ == "__main__":
    logger.debug('Start application')
    app = Application()
    server = HTTPServer(app)

    signal.signal(signal.SIGQUIT, app.exit_handler)
    signal.signal(signal.SIGTERM, app.exit_handler)
    signal.signal(signal.SIGINT, app.exit_handler)

    server.listen(app.APP_PORT)
    logger.debug(f'Listening on port {app.APP_PORT}')
    ioloop.IOLoop.current().start()
