from tornado.testing import gen_test

from word_counter.models import Word
from utils.test_helper import TestHandlerBase


class TestAdminWordListHandler(TestHandlerBase):
    @gen_test
    def test_get_empty_page(self):
        response = yield self.http_client.fetch(
            self.get_url('/admin/')
        )
        self.assertIn('Words not found', response.body.decode('utf-8'))

    @gen_test
    def test_word_in_list(self):
        words = [('test_1', 5), ('test_2', 3)]
        yield Word.bulk_insert_update(words, self.application)

        response = yield self.http_client.fetch(
            self.get_url('/admin/')
        )
        self.assertIn('test_1', response.body.decode('utf-8'))
        self.assertIn('test_2', response.body.decode('utf-8'))

    @gen_test
    def test_pagination(self):
        words = [('test_2', 4), ('test_3', 3), ('test_4', 2), ('test_1', 5)]
        yield Word.bulk_insert_update(words, self.application)

        response = yield self.http_client.fetch(
            self.get_url('/admin/')
        )
        self.assertIn('test_1', response.body.decode('utf-8'))
        self.assertIn('test_2', response.body.decode('utf-8'))
        self.assertNotIn('test_3', response.body.decode('utf-8'))
        self.assertNotIn('test_4', response.body.decode('utf-8'))

        response = yield self.http_client.fetch(
            self.get_url('/admin/?page=1')
        )
        self.assertIn('test_1', response.body.decode('utf-8'))
        self.assertIn('test_2', response.body.decode('utf-8'))
        self.assertNotIn('test_3', response.body.decode('utf-8'))
        self.assertNotIn('test_4', response.body.decode('utf-8'))

        response = yield self.http_client.fetch(
            self.get_url('/admin/?page=2')
        )
        self.assertNotIn('test_1', response.body.decode('utf-8'))
        self.assertNotIn('test_2', response.body.decode('utf-8'))
        self.assertIn('test_3', response.body.decode('utf-8'))
        self.assertIn('test_4', response.body.decode('utf-8'))

    @gen_test
    def test_pagination_invalid_params(self):
        words = [('test_2', 4), ('test_3', 3), ('test_4', 2), ('test_1', 5)]
        yield Word.bulk_insert_update(words, self.application)

        response = yield self.http_client.fetch(
            self.get_url('/admin/?page=invalid')
        )
        self.assertIn('test_1', response.body.decode('utf-8'))
        self.assertIn('test_2', response.body.decode('utf-8'))
        self.assertNotIn('test_3', response.body.decode('utf-8'))
        self.assertNotIn('test_4', response.body.decode('utf-8'))

        response = yield self.http_client.fetch(
            self.get_url('/admin/?page=-1')
        )
        self.assertIn('test_1', response.body.decode('utf-8'))
        self.assertIn('test_2', response.body.decode('utf-8'))
        self.assertNotIn('test_3', response.body.decode('utf-8'))
        self.assertNotIn('test_4', response.body.decode('utf-8'))
