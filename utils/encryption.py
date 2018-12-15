import os

import base64
from Crypto import Random
from Crypto.PublicKey import RSA


class Encryption:
    def __init__(self, app):
        self.app = app
        self.pub_key = None
        self.secret_key = None
        self.public_key = app.PUBLIC_KEY
        self.private_key = app.PRIVATE_KEY

        if not all([os.path.exists(self.public_key), os.path.exists(self.private_key)]):
            self.generate_keys()
        else:
            self.read_keys()

    def _write_key(self, filename, key):
        with open(filename, 'wb') as f:
            try:
                f.write(key.exportKey())
            except Exception as e:
                raise e

    def _read_key(self, filename):
        rsa = RSA.RSAImplementation()
        with open(filename, 'rb') as f:
            try:
                key = f.read()
                key = rsa.importKey(key)
            except Exception as e:
                raise e
            else:
                return key

    def generate_keys(self):
        # RSA modulus length must be a multiple of 256 and >= 1024
        modulus_length = 256 * 4  # use larger value in production
        self.secret_key = RSA.generate(modulus_length, Random.new().read)
        self.pub_key = self.secret_key.publickey()

        self._write_key(self.public_key, self.pub_key)
        self._write_key(self.private_key, self.secret_key)

    def read_keys(self):
        self.pub_key = self._read_key(self.public_key)
        self.secret_key = self._read_key(self.private_key)

    def encrypt_message(self, msg):
        encrypted_msg = self.pub_key.encrypt(msg.encode('utf-8'), 32)[0]
        # base64 encoded strings are database friendly
        encoded_encrypted_msg = base64.b64encode(encrypted_msg)
        return encoded_encrypted_msg

    def decrypt_message(self, msg):
        decoded_encrypted_msg = base64.b64decode(msg)
        decoded_decrypted_msg = self.secret_key.decrypt(decoded_encrypted_msg)
        return decoded_decrypted_msg.decode('utf-8')
