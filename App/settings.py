def get_db_url(db_info):
    ENGINE = db_info.get('ENGINE') or 'mysql'
    DRIVER = db_info.get('DRIVER') or 'pymysql'
    USER = db_info.get('USER') or 'root'
    PASSWORD = db_info.get('PASSWORD') or 'root'
    HOST = db_info.get('HOST') or 'localhost'
    PORT = db_info.get('PORT') or '3306'
    NAME = db_info.get('NAME') or 'RealTime'

    return '{}+{}://{}:{}@{}:{}/{}'.format(ENGINE, DRIVER, USER, PASSWORD, HOST, PORT, NAME)


class Config:
    DEBUG = False
    TESTING = False
    # 跟踪SqlAlchemy的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    from os import urandom  # 产生随机字符串
    SECRET_KEY = urandom(24)  # 密银必须是24个字符


class DevelopConfig(Config):
    # 开发环境
    DEBUG = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'Qwerty-0',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'RealTime'
    }
    SQLALCHEMY_DATABASE_URI = 'sqlite:///RealTime.db'  # get_db_url(DATABASE)


class TestingConfig(Config):
    # 测试环境
    TESTING = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'Qwerty-0',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'RealTime'
    }
    SQLALCHEMY_DATABASE_URI = get_db_url(DATABASE)


class ProductConfig(Config):
    # 线上环境
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'Qwerty-0',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'RealTime'
    }
    SQLALCHEMY_DATABASE_URI = get_db_url(DATABASE)


envs = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'product': ProductConfig,

    'default': DevelopConfig
}
