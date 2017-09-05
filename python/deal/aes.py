#! -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


class AESCipher:
    def __init__(self, key, model):
        self.key = key
        self.model = model

    def encrypt(self, raw):
        raw = pad(raw)
        iv = '0000000000000000'
        cipher = AES.new(self.key, self.model, iv)
        encrypt_txt = cipher.encrypt(raw)
        return base64.b64encode(encrypt_txt)

    def decrypt(self, enc):
        iv = '0000000000000000'
        b_dec = base64.b64decode(enc)
        cipher = AES.new(self.key, self.model, iv)
        plaintext = cipher.decrypt(b_dec[16:])
        return unpad(plaintext)
