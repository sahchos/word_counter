import os

from utils.test_helper import TestHandlerBase


class TestEncryption(TestHandlerBase):
    def setUp(self):
        super().setUp()
        self.public_path = os.path.join(self.application.APP_ROOT, self.application.PUBLIC_KEY)
        self.private_path = os.path.join(self.application.APP_ROOT, self.application.PRIVATE_KEY)

    def tearDown(self):
        super().tearDown()
        if os.path.exists(self.public_path):
            os.remove(self.public_path)

        if os.path.exists(self.private_path):
            os.remove(self.private_path)

    def test_generate_keys(self):
        self.assertFalse(os.path.exists(self.public_path))
        self.assertFalse(os.path.exists(self.private_path))
        self.application.encryption.generate_keys()
        self.assertTrue(os.path.exists(self.public_path))
        self.assertTrue(os.path.exists(self.private_path))

    def test_read_existing_keys(self):
        self.application.encryption.generate_keys()
        generated_pub_key = self.application.encryption.pub_key
        generated_secret_key = self.application.encryption.secret_key

        self.application.encryption.read_keys()
        self.assertEqual(generated_pub_key, self.application.encryption.pub_key)
        self.assertEqual(generated_secret_key, self.application.encryption.secret_key)

    def test_encrypt_decrypt_msg(self):
        text = 'text'
        encrypted_text = self.application.encryption.encrypt_message(text)
        self.assertNotEqual(text, encrypted_text)

        decrypted_text = self.application.encryption.decrypt_message(encrypted_text)
        self.assertEqual(text, decrypted_text)
