import hashlib

from utils.encryption import Encryption


class Word:
    def __init__(self, word, count):
        self.word = word
        self.count = count

    def get_encrypted_word(self, encryption):
        return encryption.encrypt_message(self.word)

    def get_decrypted_word(self, encryption):
        return encryption.decrypt_message(self.word)

    def get_hashed_word(self, app):
        return hashlib.sha512(app.WORD_SALT.encode('utf-8') + self.word.encode('utf-8')).hexdigest()

    @classmethod
    async def bulk_insert_update(cls, words, app):
        sql = """
            INSERT INTO `words` (`pk`, `word`, `count`) VALUES (%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    `count` = VALUES(`count`);
        """

        words_data = []
        encryption = Encryption(app)
        for word in words:
            w = cls(*word)
            words_data.append((w.get_hashed_word(app), w.get_encrypted_word(encryption), w.count))

        await app.db.executemany(sql, words_data)
