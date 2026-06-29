"""
用户模型 (User)
支持多角色：普通用户(user) + 管理员(admin)
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """用户表 — 存储所有注册用户信息，支持角色权限区分"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(256), default='default_avatar.png')
    bio = db.Column(db.Text, default='')
    # 角色字段：user(普通用户) / admin(管理员)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------- 关系 ----------
    # 用户上传的歌曲
    songs = db.relationship('Song', backref='uploader', lazy='dynamic',
                            cascade='all, delete-orphan')
    # 用户的歌单
    playlists = db.relationship('Playlist', backref='owner', lazy='dynamic',
                                cascade='all, delete-orphan')
    # 用户的评论
    comments = db.relationship('Comment', backref='author', lazy='dynamic',
                               cascade='all, delete-orphan')
    # 用户的收藏
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic',
                                cascade='all, delete-orphan')

    def set_password(self, password):
        """使用 Werkzeug 哈希存储密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """判断是否为管理员"""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
