"""
用户认证控制器 — 注册/登录/登出
支持多角色：注册时默认为普通用户(user)，管理员由系统预设
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册 — 默认角色为 user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        # 表单验证
        errors = []
        if not username or len(username) < 2 or len(username) > 80:
            errors.append('用户名长度须在 2-80 个字符之间。')
        if not email or '@' not in email:
            errors.append('请输入有效的邮箱地址。')
        if len(password) < 6:
            errors.append('密码长度不能少于 6 位。')
        if password != password2:
            errors.append('两次输入的密码不一致。')
        if User.query.filter_by(username=username).first():
            errors.append('该用户名已被注册。')
        if User.query.filter_by(email=email).first():
            errors.append('该邮箱已被注册。')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html', username=username, email=email)

        # 创建用户（默认角色为 user）
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('注册成功！请登录。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录 — 支持普通用户和管理员统一登录入口"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('用户名或密码错误。', 'danger')
            return render_template('auth/login.html', username=username)

        login_user(user, remember=remember)
        flash(f'欢迎回来，{user.username}！', 'success')

        # 管理员登录后跳转到后台
        next_page = request.args.get('next')
        if user.is_admin():
            if next_page:
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功退出登录。', 'info')
    return redirect(url_for('main.index'))
