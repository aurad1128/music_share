"""
音乐分享与推荐网站 — 配置文件
基于 Flask 配置模式，包含开发环境所有必需配置项
"""
import os

# 项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基础配置（所有环境共用）"""
    # Flask 密钥 — 用于 session 签名和 CSRF 保护
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'music-share-secret-key-2026'

    # SQLite 数据库路径
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'music_share.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件上传配置
    UPLOADED_COVERS_DEST = os.path.join(BASE_DIR, 'static', 'uploads', 'covers')
    UPLOADED_COVERS_ALLOW = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传 16MB

    # 分页配置
    SONGS_PER_PAGE = 12
    COMMENTS_PER_PAGE = 10

    # 音乐风格列表（题目要求：流行/摇滚/说唱/电子/古典等）
    MUSIC_STYLES = ['流行', '摇滚', '说唱', '电子', '古典', '民谣', '爵士', 'R&B', '其他']
