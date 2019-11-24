from functools import wraps
from flask import redirect, session, url_for

# 验证登录
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper