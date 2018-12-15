from utils.test_helper import TestHandlerBase
from utils.text_processor import TextProcessor


class TestTextProcessor(TestHandlerBase):
    def test_set_text(self):
        text = '<p>text from p tag</p><div>Division text</div><a>link</a>'
        processor = TextProcessor(text)
        processor.set_text()
        self.assertEqual(processor.text, 'text from p tag Division text link')

    def test_get_word_counter(self):
        text = '<p>text from p tag a an the text</p><div>Division text division</div><a>link</a>'
        processor = TextProcessor(text)
        processor.set_text()
        word_counter = processor.get_word_counter(['N', 'V'])
        word_counter_keys = word_counter.keys()
        self.assertEqual(len(word_counter), 4)
        self.assertEqual(word_counter['text'], 3)
        self.assertEqual(word_counter['division'], 2)
        self.assertEqual(word_counter['tag'], 1)
        self.assertEqual(word_counter['link'], 1)
        self.assertNotIn('from', word_counter_keys)
        self.assertNotIn('p', word_counter_keys)
        self.assertNotIn('a', word_counter_keys)
        self.assertNotIn('an', word_counter_keys)
        self.assertNotIn('the', word_counter_keys)
        self.assertNotIn('the', word_counter_keys)
