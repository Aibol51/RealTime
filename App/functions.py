from .models import *

from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from urllib import parse
from re import match
import string

AES_SECRET_KEY = 'aesJM_Yernar2020'  # 必须为16/24/32个字符
IV = "1234567890123456"

# padding算法
BS = len(AES_SECRET_KEY)
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1:])]

class AES_ENCRYPT(object):
    def __init__(self):
        self.key = AES_SECRET_KEY
        self.mode = AES.MODE_CBC
    # 加密
    def encrypt(self, text):
        cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))
        # AES加密时候得到的字符串不一定是ascii字符集的,
        # 输出到终端或者保存时候可能存在问题, 所以使用base64编码;
        return b64encode(self.ciphertext)
    # 解密
    def decrypt(self, text):
        decode = b64decode(text)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        return unpad(plain_text)

############################
############################
############################

def detection(need: str, value):
    '''
    :param need: 需要检测的值的类型(name, email, pwd...)
    :param value: 需要检测的值
    :return: True / False
    '''
    ALLOWED_WORD = string.ascii_letters + string.digits + '_'

    if need == 'name' or need == 'pwd':
        if len(value) <= 32 and len(value) > 0:
            for word in value:
                if word in ALLOWED_WORD:
                    pass
                else:
                    return False
            return True
        else:
            return False

    elif need == 'email':
        email_format = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if match(email_format, value):
            return True
        else:
            return False

    else:
        return False


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'PNG', 'JPG', 'gif', 'GIF'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS