import signal

import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpserver import HTTPServer

from utils.db import Database


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        sql = "SELECT table_name FROM information_schema.tables;"
        res = await app.db.query(sql)
        print(res)
        self.write("Hello world")
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
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
        server.stop()
        # TODO: use env
        # in real app could be extended to request endpoint for check active requests count
        await gen.sleep(5)
        tornado.ioloop.IOLoop.current().stop()
        self.db.pool.close()

    def exit_handler(self, sig, frame):
        tornado.ioloop.IOLoop.current().add_callback_from_signal(self._shutdown)


if __name__ == "__main__":
    app = Application()
    server = HTTPServer(app)

    signal.signal(signal.SIGQUIT, app.exit_handler)
    signal.signal(signal.SIGTERM, app.exit_handler)
    signal.signal(signal.SIGINT, app.exit_handler)

    # TODO: use env param
    server.listen(8888)
    tornado.ioloop.IOLoop.current().start()
