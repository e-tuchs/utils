# -*- coding: utf-8 -*-
import logging
import urllib2
from hashlib import md5
from Crypto.Cipher import AES

KEY = '1234567887654321'
MODE = AES.MODE_ECB
APPEND_KEY = "0"


def mk_md5(obj, isbuff=True):
    """
    :param obj: will md5sum object
    :param isbuff: True: string , False: file
    :return:
    """
    hash_md5 = md5()
    if isbuff:
        hash_md5.update(obj)
    else:
        with open(obj, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    return hash_md5.hexdigest().upper()


class AESFactory(object):
    key, mode = None, None

    def __init__(self, key=KEY, mode=MODE):
        self.key = key
        self.mode = mode

    def encrypt(self, cleartext):
        """
        :param cleartext:  input clear text
        :return: encrypted text
        """
        encryptor = AES.new(self.key, self.mode, b'0000000000000000')
        try:
            text_len = len(cleartext)
            append_len = 16-text_len if text_len <= 16 else 16-divmod(text_len, 16)[1]
            append_str = APPEND_KEY*append_len
            text = cleartext+append_str
            ciphertext = encryptor.encrypt(text)
        except ValueError, e:
            logging.error("AES_encrypt:"+str(e))
            return None
        else:
            return ciphertext

    def decrypt(self, ciphertext):
        decryptor = AES.new(self.key, self.mode, b'0000000000000000')
        try:
            plain = decryptor.decrypt(ciphertext)
        except ValueError, e:
            logging.error("AES_decrypt:"+str(e))
            return None
        else:
            return plain

aes = AESFactory(key=KEY, mode=MODE)
cipher = aes.encrypt('0123456789abcdef')
print cipher
clear = aes.decrypt(ciphertext=cipher)
print clear
