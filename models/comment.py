"""
评论模型 (Comment)
歌曲评论区互动功能
"""
from datetime import datetime
from app import db


class Comment(db.Model):
    """评论表 — 用户对歌曲的评论"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment by user={self.user_id} on song={self.song_id}>'
