from io import BytesIO

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

from sqlalchemy import types

from settings import settings


class RsaString(types.TypeDecorator):
    '''
    Represents an immutable structure as a json-encoded string.
    '''

    impl = types.LargeBinary

    def __init__(
            self,
            public_key=settings['public_key'],
            private_key=settings['private_key']
    ):
        self.public_key = public_key
        self.private_key = private_key
        types.TypeDecorator.__init__(self)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not isinstance(value, bytes):
                value = bytes(value, 'utf-8')
            session_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(self.public_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(value)

            file = BytesIO()
            for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext):
                file.write(x)
            file.seek(0)
            return file.read()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if not isinstance(value, bytes):
                value = bytes(value, 'utf-8')
            file = BytesIO(value)
            file.seek(0)
            enc_session_key, nonce, tag, ciphertext = [
                file.read(x) for x in (self.private_key.size_in_bytes(), 16, 16, -1)
            ]

            try:
                # Decrypt the session key with the private RSA key
                cipher_rsa = PKCS1_OAEP.new(self.private_key)
                session_key = cipher_rsa.decrypt(enc_session_key)

                # Decrypt the data with the AES session key
                cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
                value = cipher_aes.decrypt(ciphertext)
            except:
                value = b''
            # value = cipher_aes.decrypt_and_verify(ciphertext, tag)
            return value.decode("utf-8")
        return value
