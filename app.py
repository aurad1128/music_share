"""
音乐分享与推荐网站 — Flask 应用入口
题目二十四：音乐分享与推荐网站
Python 程序设计课程设计 — 智科 2401-2

启动方式: python app.py  (必须用 Python 3.12)
"""
import os
import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from config import Config

# ---------- 初始化扩展 ----------
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录后再访问此页面。'
login_manager.login_message_category = 'warning'

ALLOWED_COVER_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_cover_file(filename):
    """检查上传文件是否为允许的图片格式"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_COVER_EXTENSIONS


def save_cover(file_storage, upload_folder):
    """保存封面图到指定目录，返回文件名"""
    if file_storage and file_storage.filename and allowed_cover_file(file_storage.filename):
        ext = file_storage.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(upload_folder, filename)
        file_storage.save(filepath)
        return filename
    return None


# ---------- 创建应用 ----------
app = Flask(__name__)
app.config.from_object(Config)

# 注入工具函数
app.config['save_cover'] = save_cover
app.config['allowed_cover_file'] = allowed_cover_file

# 初始化数据库
db.init_app(app)

# 初始化登录管理
login_manager.init_app(app)

# 创建上传目录
os.makedirs(app.config['UPLOADED_COVERS_DEST'], exist_ok=True)

# ---------- 必须在 db.init_app 之后导入模型 ----------
from models.user import User
from models.song import Song, Favorite
from models.playlist import Playlist, PlaylistSong
from models.comment import Comment
from models.browse_record import BrowseRecord
from models.follow import Follow

# ---------- 注册蓝图 ----------
from controllers.auth import auth_bp
from controllers.main import main_bp
from controllers.song import song_bp
from controllers.admin import admin_bp
from controllers.playlist import playlist_bp
from controllers.comment import comment_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(song_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(comment_bp)


# ---------- Flask-Login 用户加载器 ----------
@login_manager.user_loader
def load_user(user_id):
    """根据用户 ID 加载用户对象"""
    return User.query.get(int(user_id))


# ---------- 自定义错误页面 ----------
from flask import render_template

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ---------- 初始化数据库表 ----------
with app.app_context():
    db.create_all()

# 启动入口请使用 run.py，避免 double-import 问题
