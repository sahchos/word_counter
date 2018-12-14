import os
import string
from collections import defaultdict, Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


class TextProcessor:
    def __init__(self, text):
        self.text = text
        self.nltk_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nltk_data')
        if self.nltk_data_path not in nltk.data.path:
            nltk.data.path.append(self.nltk_data_path)

    def set_text_from_tags(self, tags):
        """
        Extract text from specified tags and set processor text.
        :param list tags: list of tags to extract text
        """
        soup = BeautifulSoup(self.text, features='html.parser')
        self.text = ''.join(''.join(s.findAll(text=True)) for s in soup.findAll(tags))

    def get_word_counter(self, tags):
        """
        Get word counter of words found in text exclude stopwords.
        :param list tags: nltk specific one character tags
        :return Counter: word counter
        """
        tokens = [word for (word, pos) in nltk.pos_tag(word_tokenize(self.text)) if pos[0] in tags]
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation from each word
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic or letters
        words = [word for word in stripped if word.isalpha() and len(word) > 1]

        word_counter = defaultdict(int)
        for word in words:
            if word in stopwords.words('english'):
                continue

            word_counter[word] += 1

        return Counter(word_counter)
