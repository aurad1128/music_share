"""
歌单控制器 — 创建/管理个人歌单（P2 扩展完善）
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.playlist import Playlist, PlaylistSong
from models.song import Song
from app import db

playlist_bp = Blueprint('playlist', __name__, url_prefix='/playlist')


@playlist_bp.route('/')
@login_required
def my_playlists():
    """我的歌单列表"""
    playlists = Playlist.query.filter_by(user_id=current_user.id).order_by(
        Playlist.created_at.desc()).all()
    return render_template('playlists/my.html', playlists=playlists)


@playlist_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建新歌单"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        is_public = request.form.get('is_public') == 'on'

        if not name:
            flash('请输入歌单名称。', 'danger')
            return render_template('playlists/create.html')

        playlist = Playlist(
            name=name,
            description=description,
            user_id=current_user.id,
            is_public=is_public
        )
        db.session.add(playlist)
        db.session.commit()
        flash(f'歌单《{name}》创建成功！', 'success')
        return redirect(url_for('playlist.my_playlists'))

    return render_template('playlists/create.html')


@playlist_bp.route('/<int:playlist_id>')
def detail(playlist_id):
    """歌单详情"""
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template('playlists/detail.html', playlist=playlist)


@playlist_bp.route('/<int:playlist_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(playlist_id):
    """编辑歌单"""
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        flash('您无权编辑此歌单。', 'danger')
        return redirect(url_for('playlist.my_playlists'))

    if request.method == 'POST':
        playlist.name = request.form.get('name', '').strip()
        playlist.description = request.form.get('description', '').strip()
        playlist.is_public = request.form.get('is_public') == 'on'
        db.session.commit()
        flash('歌单更新成功！', 'success')
        return redirect(url_for('playlist.detail', playlist_id=playlist_id))

    return render_template('playlists/edit.html', playlist=playlist)


@playlist_bp.route('/<int:playlist_id>/delete', methods=['POST'])
@login_required
def delete(playlist_id):
    """删除歌单"""
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        flash('您无权删除此歌单。', 'danger')
        return redirect(url_for('playlist.my_playlists'))

    db.session.delete(playlist)
    db.session.commit()
    flash('歌单已删除。', 'info')
    return redirect(url_for('playlist.my_playlists'))


@playlist_bp.route('/<int:playlist_id>/add_song/<int:song_id>', methods=['POST'])
@login_required
def add_song(playlist_id, song_id):
    """向歌单添加歌曲"""
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        flash('您无权操作此歌单。', 'danger')
        return redirect(url_for('playlist.my_playlists'))

    exists = PlaylistSong.query.filter_by(
        playlist_id=playlist_id, song_id=song_id).first()
    if exists:
        flash('该歌曲已在歌单中。', 'warning')
    else:
        ps = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(ps)
        db.session.commit()
        flash('歌曲已添加到歌单。', 'success')

    return redirect(request.referrer or url_for('playlist.detail', playlist_id=playlist_id))


@playlist_bp.route('/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
@login_required
def remove_song(playlist_id, song_id):
    """从歌单移除歌曲"""
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        flash('您无权操作此歌单。', 'danger')
        return redirect(url_for('playlist.my_playlists'))

    ps = PlaylistSong.query.filter_by(
        playlist_id=playlist_id, song_id=song_id).first()
    if ps:
        db.session.delete(ps)
        db.session.commit()
        flash('歌曲已从歌单中移除。', 'info')

    return redirect(url_for('playlist.detail', playlist_id=playlist_id))
