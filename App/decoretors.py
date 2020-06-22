'''
    用于储存装饰器
'''
from functools import wraps
from flask import (session,
                   redirect, url_for)

# 管理员(Admin)の登录限制的装饰器
def adminLogRequired(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('admin_login'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('home_blue.reg_log'))
    return wrapper