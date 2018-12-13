import signal
import logging
import logging.config

import tornado.web
import tornado.gen
import tornado.ioloop
from tornado.httpserver import HTTPServer

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
        logger.debug('Create DB connection pool')
        # TODO: read and pass env settings
        self.db = Database(host='db', port=3306, user='admin', password='admin', database='octopus')
        # TODO: get handlers from apps
        handlers = [
            (r"/", MainHandler),
        ]
        # TODO: use env settings
        settings = dict(
            debug=True
        )
        super().__init__(handlers=handlers, **settings)

    async def _shutdown(self):
        # stop receive requests
        logger.debug('Shutdown stop server')
        server.stop()

        # TODO: use env
        # in real app could be extended to request endpoint for check active requests count
        logger.debug('Shutdown waiting to process existing requests')
        await tornado.gen.sleep(5)
        tornado.ioloop.IOLoop.current().stop()

        logger.debug('Shutdown close pool connection')
        self.db.pool.close()

    def exit_handler(self, sig, frame):
        logger.debug(f'Shutdown signal received {sig}')
        tornado.ioloop.IOLoop.current().add_callback_from_signal(self._shutdown)


if __name__ == "__main__":
    logger.debug('Start application')
    app = Application()
    server = HTTPServer(app)

    signal.signal(signal.SIGQUIT, app.exit_handler)
    signal.signal(signal.SIGTERM, app.exit_handler)
    signal.signal(signal.SIGINT, app.exit_handler)

    # TODO: use env param
    server.listen(8888)
    tornado.ioloop.IOLoop.current().start()
