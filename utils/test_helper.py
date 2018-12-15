from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from app import Application


class TestApplication(Application):
    def __init__(self):
        super().__init__()
        self.TOP_WORDS_COUNT = 5
        self.ADMIN_WORDS_PER_PAGE = 2

    def _set_env_config(self):
        """Custom _create_tables to set test db"""
        super()._set_env_config()
        self.MYSQL_DATABASE = 'octopus_test'
        self.MYSQL_USER = 'root'
        self.MYSQL_PASSWORD = self.MYSQL_ROOT_PASSWORD
        self.PUBLIC_KEY = 'test_key_rsa.pub'
        self.PRIVATE_KEY = 'test_key_rsa'


app = TestApplication()


class TestHandlerBase(AsyncHTTPTestCase):
    async def _clear_db(self):
        await self.application.db.execute("DELETE FROM `words`")

    def get_new_ioloop(self):
        return IOLoop.current()

    def setUp(self):
        self.application = app
        super().setUp()

    def tearDown(self):
        IOLoop.current().add_callback(self._clear_db)
        super().tearDown()

    def get_app(self):
        server = HTTPServer(app)
        return server
