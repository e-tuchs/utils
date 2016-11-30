# -*- coding: utf-8 -*-
import logging
from hashlib import md5
from Crypto.Cipher import AES
from functools import wraps


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
        encryptor = AES.new(self.key, self.mode, b'0000000000000000')
        try:
            text_len = len(cleartext)
            append_len = 16-text_len if text_len <= 16 else 16-divmod(text_len, 16)[1]
            append_str = self.append_str*append_len
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


def decrypt_response(key_mode):
    """
    :param key_mode:{"KEY": keystr, "MODE": aesmod eg:ECB, 'METHOD': POST or GET, "REPLACE": replace_str, eg:"@"}
    :return:
    """
    def decorator(func):
        def inner(request, *args, **kwargs):
            try:
                _raw = request.raw_post_data
                _aes = AESFactory(key=key_mode['KEY'], mode=key_mode['MODE'], append_str=key_mode['REPLACE'])
                _text = _aes.decrypt(ciphertext=_raw)
                _repstr = key_mode['REPLACE']
                cleartext = _text.replace(_repstr, '')
                _dict = {}
                for rq in cleartext.split('&'):
                    _dict[rq.split('=')[0]] = rq.split('=')[1]
            except Exception, e:
                logging.error(e)
                return {"status": 400, "detail": "decrypt error"}
            else:
                if key_mode['METHOD'] == 'POST':
                    request.POST = dict(request.POST, **_dict)
                else:
                    request.GET = dict(request.GET, **_dict)
            return func(request, *args, **kwargs)
        return wraps(func, )(inner)
    return decorator
