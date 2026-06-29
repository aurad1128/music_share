"""
浏览记录模型 (BrowseRecord)
用于猜你喜欢推荐功能的数据基础
记录用户浏览/点击歌曲的行为
"""
from datetime import datetime
from app import db


class BrowseRecord(db.Model):
    """浏览记录表 — 记录用户浏览歌曲的行为，为推荐算法提供数据"""
    __tablename__ = 'browse_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    browse_count = db.Column(db.Integer, default=1)
    last_browsed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    song = db.relationship('Song', backref='browse_records', lazy=True)

    # 联合唯一索引
    __table_args__ = (
        db.UniqueConstraint('user_id', 'song_id', name='uq_user_song_browse'),
    )

    def __repr__(self):
        return f'<BrowseRecord user={self.user_id} song={self.song_id} count={self.browse_count}>'
