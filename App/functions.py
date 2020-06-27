from .models import *

from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from urllib import parse
from re import match
import string
from datetime import datetime

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

def calc_view():
    # 获取用户的IP地址
    statistic = Statistics.query.filter(Statistics.ip_addr == request.remote_addr).first()
    if statistic: # 此IP地址的上次浏览时间和现在时间做比较, >=1 天的话浏览量+1并把上次浏览时间改为当前时间;
        if (datetime.strptime(str(datetime.now()), '%Y-%m-%d') - datetime.strptime(statistic.create_time, '%Y-%m-%d')).days >= 1:
            statistic.create_time = str(datetime.now())
            visit = Visit.query.filter(Visit.id == 1).first()
            visit.visit_num += 1
            db.session.commit()
    else:
        statistic = Statistics()
        statistic.ip_addr = request.remote_addr
        db.session.add(statistic)

        visit = Visit.query.filter(Visit.id == 1).first()
        visit.visit_num += 1
        db.session.commit()

    # 每隔3天清理长时间未登录的IP地址
    if (datetime.strptime(str(datetime.now()), '%Y-%m-%d') -
        datetime.strptime((Visit.query.filter(Visit.id == 1).first()).clean_time, '%Y-%m-%d')).days >= 3:

        for addr in range(Statistics.query.all()):
        # IP地址两天未登录就删掉
            if (datetime.strptime(str(datetime.now()), '%Y-%m-%d') - datetime.strptime(addr.create_time, '%Y-%m-%d')).days >= 2:
                db.session.delete(addr); db.session.commit();
