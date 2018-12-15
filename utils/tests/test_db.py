from tornado.testing import gen_test

from utils.test_helper import TestHandlerBase
from word_counter.models import Word


class TestDB(TestHandlerBase):
    @gen_test
    def test_execute(self):
        words = [('test_2', 4)]
        yield Word.bulk_insert_update(words, self.application)

        result = yield self.application.db.execute("SELECT COUNT(*) FROM words")
        self.assertEqual(result, 1)

    @gen_test
    def test_executemany(self):
        words = [('test_2', 4), ('test_3', 3), ('test_4', 2), ('test_1', 5)]
        yield Word.bulk_insert_update(words, self.application)

        result = yield self.application.db.get("SELECT COUNT(*) FROM words")
        self.assertEqual(len(words), result['COUNT(*)'])

    @gen_test
    def test_get(self):
        words = [('test_2', 4), ('test_3', 3), ('test_4', 2), ('test_1', 5)]
        yield Word.bulk_insert_update(words, self.application)

        result = yield self.application.db.get("SELECT COUNT(*) FROM words")
        self.assertEqual(len(words), result['COUNT(*)'])

    @gen_test
    def test_insert(self):
        yield self.application.db.insert("INSERT INTO `words` (`pk`, `word`, `count`) VALUES ('text', 'text', 1)")

        result = yield self.application.db.execute("SELECT COUNT(*) FROM words")
        self.assertEqual(result, 1)

    @gen_test
    def test_query(self):
        yield self.application.db.insert("INSERT INTO `words` (`pk`, `word`, `count`) VALUES ('text', 'text', 1)")

        result = yield self.application.db.query("SELECT * FROM words")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['pk'], 'text')
        self.assertEqual(result[0]['word'], 'text')
        self.assertEqual(result[0]['count'], 1)
