# -*- coding: utf-8 -*-
import logging
from hashlib import md5
from Crypto.Cipher import AES
from functools import wraps
from binascii import b2a_hex, a2b_hex


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
    key, mode, append_str = None, None, None

    def __init__(self, key, mode, append_str):
        self.key = key
        self.mode = mode
        self.append_str = append_str

    def encrypt(self, cleartext):
        """
        :param cleartext:  input clear text
        :return: encrypted text
        """
        encryptor = AES.new(self.key, self.mode,)
        try:
            text_len = len(cleartext)
            append_len = 16-text_len if text_len <= 16 else 16-divmod(text_len, 16)[1]
            text = cleartext+self.append_str*append_len
            ciphertext = encryptor.encrypt(text)
        except ValueError, e:
            logging.error("AES_encrypt:"+str(e))
            return None
        else:
            return b2a_hex(ciphertext)

    def decrypt(self, ciphertext):
        decryptor = AES.new(self.key, self.mode, )
        try:
            plain = decryptor.decrypt(a2b_hex(ciphertext))
        except ValueError, e:
            logging.error("AES_decrypt:"+str(e))
            return None
        else:
            return plain


def decrypt_aes_response(key_mode):
    """
    :param key_mode:{"KEY": keystr, "MODE": aesmod eg:ECB, "REPLACE": replace_str, eg:"@", "METHOD": "POST" or "GET"}
    :return: AES_DATA in request
    """
    def decorator(func):
        def inner(request, *args, **kwargs):
            try:
                if key_mode['METHOD'] == "GET":
                    _raw = '' if not request.GET.keys() else request.GET.keys()[0]
                else:
                    _raw = request.raw_post_data
                _aes = AESFactory(key=key_mode['KEY'], mode=key_mode['MODE'], append_str=key_mode['REPLACE'])
                _text = _aes.decrypt(ciphertext=_raw)
                _cleartext = _text.replace(key_mode['REPLACE'], '')
                _dict = {}
                for rq in _cleartext.split('&'):
                    _dict[rq.split('=')[0]] = rq.split('=')[1]
            except Exception, e:
                logging.error(e)
                return {"status": 400, "detail": u"无法解析请求"}
            else:
                setattr(request, 'AES_DATA', _dict)
            return func(request, *args, **kwargs)
        return wraps(func, )(inner)
    return decorator
