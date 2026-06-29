"""
歌曲管理控制器 — 上传/查看/编辑/删除歌曲
"""
import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models.song import Song, Favorite
from models.browse_record import BrowseRecord
from models.comment import Comment
from app import db
from config import Config

song_bp = Blueprint('song', __name__, url_prefix='/song')


@song_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """上传音乐作品 — 歌曲名称/歌手/专辑/封面图/音频链接/风格"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        artist = request.form.get('artist', '').strip()
        album = request.form.get('album', '').strip()
        audio_url = request.form.get('audio_url', '').strip()
        style = request.form.get('style', '其他')
        description = request.form.get('description', '').strip()

        # 验证必填字段
        errors = []
        if not title:
            errors.append('请输入歌曲名称。')
        if not artist:
            errors.append('请输入歌手名称。')
        if style not in Config.MUSIC_STYLES:
            style = '其他'

        # 处理封面图上传
        cover_filename = ''
        if 'cover_image' in request.files:
            cover_file = request.files['cover_image']
            if cover_file and cover_file.filename:
                save_cover = current_app.config.get('save_cover')
                if save_cover:
                    result = save_cover(cover_file, current_app.config['UPLOADED_COVERS_DEST'])
                    if result:
                        cover_filename = result
                    else:
                        errors.append('封面上传失败，请检查文件格式（支持 png/jpg/gif/webp）。')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('songs/upload.html', styles=Config.MUSIC_STYLES,
                                 title=title, artist=artist, album=album,
                                 audio_url=audio_url, style=style,
                                 description=description)

        # 创建歌曲记录
        song = Song(
            title=title,
            artist=artist,
            album=album,
            cover_image=cover_filename,
            audio_url=audio_url,
            style=style,
            description=description,
            uploader_id=current_user.id
        )
        db.session.add(song)
        db.session.commit()

        flash(f'歌曲《{title}》上传成功！', 'success')
        return redirect(url_for('song.detail', song_id=song.id))

    return render_template('songs/upload.html', styles=Config.MUSIC_STYLES)


@song_bp.route('/<int:song_id>')
def detail(song_id):
    """歌曲详情页 — 展示歌曲完整信息 + 评论/收藏入口"""
    song = Song.query.get_or_404(song_id)

    # 播放计数 +1（每次访问详情页）
    song.play_count += 1
    db.session.commit()

    # 记录浏览行为（登录用户）
    if current_user.is_authenticated:
        record = BrowseRecord.query.filter_by(
            user_id=current_user.id, song_id=song_id).first()
        if record:
            record.browse_count += 1
            record.last_browsed_at = datetime.utcnow()
        else:
            record = BrowseRecord(user_id=current_user.id, song_id=song_id)
            db.session.add(record)
        db.session.commit()

    # 检查当前用户是否已收藏
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = Favorite.query.filter_by(
            user_id=current_user.id, song_id=song_id).first() is not None

    # 获取同风格推荐歌曲
    related_songs = Song.query.filter(
        Song.style == song.style,
        Song.id != song.id
    ).order_by(Song.favorite_count.desc()).limit(5).all()

    # 获取评论（按时间倒序）
    comments = Comment.query.filter_by(song_id=song_id).order_by(
        Comment.created_at.desc()).limit(20).all()

    return render_template('songs/detail.html',
                         song=song,
                         is_favorited=is_favorited,
                         related_songs=related_songs,
                         comments=comments)


@song_bp.route('/<int:song_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(song_id):
    """编辑歌曲 — 仅上传者可编辑"""
    song = Song.query.get_or_404(song_id)

    # 权限验证：只有上传者和管理员可以编辑
    if song.uploader_id != current_user.id and not current_user.is_admin():
        flash('您无权编辑此歌曲。', 'danger')
        return redirect(url_for('song.detail', song_id=song_id))

    if request.method == 'POST':
        song.title = request.form.get('title', '').strip()
        song.artist = request.form.get('artist', '').strip()
        song.album = request.form.get('album', '').strip()
        song.audio_url = request.form.get('audio_url', '').strip()
        style = request.form.get('style', '其他')
        song.style = style if style in Config.MUSIC_STYLES else '其他'
        song.description = request.form.get('description', '').strip()

        # 处理封面图更新
        if 'cover_image' in request.files:
            cover_file = request.files['cover_image']
            if cover_file and cover_file.filename:
                save_cover = current_app.config.get('save_cover')
                if save_cover:
                    result = save_cover(cover_file, current_app.config['UPLOADED_COVERS_DEST'])
                    if result:
                        # 删除旧封面
                        if song.cover_image:
                            old_path = os.path.join(
                                current_app.config['UPLOADED_COVERS_DEST'], song.cover_image)
                            if os.path.exists(old_path):
                                os.remove(old_path)
                        song.cover_image = result

        db.session.commit()
        flash(f'歌曲《{song.title}》更新成功！', 'success')
        return redirect(url_for('song.detail', song_id=song_id))

    return render_template('songs/edit.html', song=song, styles=Config.MUSIC_STYLES)


@song_bp.route('/<int:song_id>/delete', methods=['POST'])
@login_required
def delete(song_id):
    """删除歌曲 — 仅上传者和管理员可删除"""
    song = Song.query.get_or_404(song_id)

    if song.uploader_id != current_user.id and not current_user.is_admin():
        flash('您无权删除此歌曲。', 'danger')
        return redirect(url_for('song.detail', song_id=song_id))

    # 删除封面文件
    if song.cover_image:
        cover_path = os.path.join(
            current_app.config['UPLOADED_COVERS_DEST'], song.cover_image)
        if os.path.exists(cover_path):
            os.remove(cover_path)

    title = song.title
    db.session.delete(song)
    db.session.commit()
    flash(f'歌曲《{title}》已删除。', 'info')
    return redirect(url_for('main.index'))


@song_bp.route('/<int:song_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(song_id):
    """收藏/取消收藏歌曲"""
    song = Song.query.get_or_404(song_id)
    fav = Favorite.query.filter_by(
        user_id=current_user.id, song_id=song_id).first()

    if fav:
        db.session.delete(fav)
        song.favorite_count = max(0, song.favorite_count - 1)
        db.session.commit()
        return {'status': 'unfavorited', 'count': song.favorite_count}
    else:
        fav = Favorite(user_id=current_user.id, song_id=song_id)
        db.session.add(fav)
        song.favorite_count += 1
        db.session.commit()
        return {'status': 'favorited', 'count': song.favorite_count}
