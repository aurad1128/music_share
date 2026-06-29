"""
管理员后台控制器 — 多角色权限管理体系的管理端
仅 admin 角色可访问，实现：
- 仪表盘（数据总览）
- 用户管理（查看/禁用/删除）
- 歌曲管理（查看/删除）
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from models.song import Song, Favorite
from models.comment import Comment
from utils.decorators import admin_required
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ---------- 仪表盘 ----------
@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """管理仪表盘 — 展示系统核心统计数据"""
    total_users = User.query.count()
    total_songs = Song.query.count()
    total_comments = Comment.query.count()
    total_favorites = Favorite.query.count()
    admin_count = User.query.filter_by(role='admin').count()
    # 最近注册用户
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    # 最近上传歌曲
    recent_songs = Song.query.order_by(Song.created_at.desc()).limit(5).all()
    # 风格分布统计
    from config import Config
    style_stats = []
    for style in Config.MUSIC_STYLES:
        count = Song.query.filter_by(style=style).count()
        if count > 0:
            style_stats.append({'name': style, 'count': count})
    style_stats.sort(key=lambda x: x['count'], reverse=True)
    # 总播放量
    from sqlalchemy import func
    total_plays = db.session.query(func.sum(Song.play_count)).scalar() or 0

    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_songs=total_songs,
                         total_comments=total_comments,
                         total_favorites=total_favorites,
                         total_plays=total_plays,
                         admin_count=admin_count,
                         recent_users=recent_users,
                         recent_songs=recent_songs,
                         style_stats=style_stats)


# ---------- 用户管理 ----------
@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """用户管理列表"""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users)


@admin_bp.route('/user/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    """切换用户角色（普通用户 ↔ 管理员）"""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('不能修改自己的角色。', 'warning')
        return redirect(url_for('admin.users'))

    user.role = 'admin' if user.role == 'user' else 'user'
    db.session.commit()
    flash(f'用户 {user.username} 的角色已更新为 {user.role}。', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """删除用户及其所有关联数据"""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('不能删除自己的账户。', 'warning')
        return redirect(url_for('admin.users'))

    username = user.username
    db.session.delete(user)  # cascade 会自动清除关联数据
    db.session.commit()
    flash(f'用户 {username} 及其所有数据已删除。', 'success')
    return redirect(url_for('admin.users'))


# ---------- 歌曲管理 ----------
@admin_bp.route('/songs')
@login_required
@admin_required
def songs():
    """歌曲管理列表 — 管理员可查看和删除任何歌曲"""
    page = request.args.get('page', 1, type=int)
    songs = Song.query.order_by(Song.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin/songs.html', songs=songs)


@admin_bp.route('/song/<int:song_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_song(song_id):
    """管理员删除任意歌曲"""
    import os
    song = Song.query.get_or_404(song_id)
    # 删除封面文件
    if song.cover_image:
        from flask import current_app
        cover_path = os.path.join(
            current_app.config['UPLOADED_COVERS_DEST'], song.cover_image)
        if os.path.exists(cover_path):
            os.remove(cover_path)

    title = song.title
    db.session.delete(song)
    db.session.commit()
    flash(f'歌曲《{title}》已被管理员删除。', 'success')
    return redirect(url_for('admin.songs'))
