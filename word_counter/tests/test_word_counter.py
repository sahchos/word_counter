from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import gen_test
from tornado_mock.httpclient import patch_http_client, set_stub

from utils.test_helper import TestHandlerBase
from word_counter.models import Word


class TestWordCounterMethods(TestHandlerBase):
    def test_get(self):
        response = self.fetch(
            self.get_url('/word_counter/'),
        )
        self.assertEqual(response.code, 200)

    @gen_test
    def test_form_invalid(self):
        post_data = {'url': 'invalid'}
        response = yield self.http_client.fetch(
            self.get_url('/word_counter/'),
            method='POST',
            body=urlencode(post_data)
        )
        self.assertIn('Invalid URL'.encode('utf-8'), response.body)

    @gen_test
    def test_fetch_words(self):
        response_text = '<p>java text python from p python java text</p><div>text python run python</div>'
        app_http_client = self.application.http_client = AsyncHTTPClient(force_instance=True)
        patch_http_client(app_http_client)

        set_stub(app_http_client, 'http://example.com', response_body=response_text)

        post_data = {'url': 'http://example.com'}
        response = yield self.http_client.fetch(
            self.get_url('/word_counter/'),
            method='POST',
            body=urlencode(post_data)
        )
        self.application.http_client = AsyncHTTPClient()

        result = yield self.application.db.query("SELECT * FROM words ORDER BY `count` DESC")
        expected_words = [
            ('python', 4),
            ('text', 3),
            ('java', 2),
            ('run', 1),
        ]
        for i, word in enumerate(result):
            w = Word(word['word'], word['count'])
            self.assertEqual(expected_words[i][0], w.get_decrypted_word(self.application.encryption))
            self.assertEqual(expected_words[i][1], w.count)

        for word in expected_words:
            self.assertIn(''.join([word[0], ' - ', str(word[1])]), response.body.decode('utf-8'))
