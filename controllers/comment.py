"""
评论控制器 — 歌曲评论区互动（P2 扩展完善）
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.comment import Comment
from models.song import Song
from app import db

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')


@comment_bp.route('/song/<int:song_id>', methods=['POST'])
@login_required
def add(song_id):
    """发表评论"""
    song = Song.query.get_or_404(song_id)
    content = request.form.get('content', '').strip()

    if not content:
        flash('评论内容不能为空。', 'danger')
        return redirect(url_for('song.detail', song_id=song_id))

    if len(content) > 1000:
        flash('评论内容不能超过 1000 字。', 'danger')
        return redirect(url_for('song.detail', song_id=song_id))

    comment = Comment(
        user_id=current_user.id,
        song_id=song_id,
        content=content
    )
    db.session.add(comment)
    song.comment_count += 1
    db.session.commit()

    flash('评论发表成功！', 'success')
    return redirect(url_for('song.detail', song_id=song_id))


@comment_bp.route('/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete(comment_id):
    """删除评论 — 仅评论作者和管理员可删除"""
    comment = Comment.query.get_or_404(comment_id)
    song = Song.query.get(comment.song_id)

    if comment.user_id != current_user.id and not current_user.is_admin():
        flash('您无权删除此评论。', 'danger')
        return redirect(url_for('song.detail', song_id=comment.song_id))

    if song:
        song.comment_count = max(0, song.comment_count - 1)
    db.session.delete(comment)
    db.session.commit()

    flash('评论已删除。', 'info')
    return redirect(url_for('song.detail', song_id=comment.song_id))
