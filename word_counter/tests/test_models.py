import hashlib

from tornado.testing import gen_test

from utils.test_helper import TestHandlerBase
from word_counter.models import Word


class TestWordModel(TestHandlerBase):
    def test_get_encrypted_word(self):
        w = Word('text', 10)
        encrypted = w.get_encrypted_word(self.application.encryption)
        self.assertNotEqual(w.word, encrypted)
        self.assertNotEqual(len(w.word), len(encrypted))

    def test_get_decrypted_word(self):
        word_text = 'text'
        w = Word(word_text, 10)
        encrypted = w.get_encrypted_word(self.application.encryption)
        w.word = encrypted
        self.assertEqual(word_text, w.get_decrypted_word(self.application.encryption))

    def test_get_hashed_word(self):
        word_text = 'text'
        w = Word('text', 10)
        hashed = w.get_hashed_word(self.application)
        hashed_res = hashlib.sha512(self.application.WORD_SALT.encode('utf-8') + word_text.encode('utf-8')).hexdigest()
        self.assertEqual(hashed, hashed_res)

    @gen_test
    def test_bulk_insert_update(self):
        words = [('test_2', 4), ('test_3', 3), ('test_4', 2), ('test_1', 5)]
        yield Word.bulk_insert_update(words, self.application)

        result = yield self.application.db.get("SELECT COUNT(*) FROM words")
        self.assertEqual(len(words), result['COUNT(*)'])
