"""
权限装饰器 — 实现多角色权限隔离
- @login_required: 要求登录
- @admin_required: 要求管理员角色
"""
from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    """
    管理员权限装饰器
    必须在 @login_required 之后使用（Flask-Login 确保 current_user 已认证）
    用法：
        @login_required
        @admin_required
        def admin_view():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # Forbidden — 权限不足
        return f(*args, **kwargs)
    return decorated_function
