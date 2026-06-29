"""
歌曲模型 (Song)
音乐作品的核心数据表
"""
from datetime import datetime
from app import db


class Song(db.Model):
    """歌曲表 — 存储用户上传的音乐作品信息"""
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    artist = db.Column(db.String(200), nullable=False, index=True)
    album = db.Column(db.String(200), default='')
    cover_image = db.Column(db.String(500), default='')
    audio_url = db.Column(db.String(500), default='')
    style = db.Column(db.String(50), nullable=False, default='其他')
    description = db.Column(db.Text, default='')
    # 上传者
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 统计字段（冗余存储，便于排行榜排序）
    play_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------- 关系 ----------
    comments = db.relationship('Comment', backref='song', lazy='dynamic',
                               cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='song', lazy='dynamic',
                                cascade='all, delete-orphan')

    def to_dict(self):
        """转为字典，方便 JSON 序列化"""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'cover_image': self.cover_image,
            'audio_url': self.audio_url,
            'style': self.style,
            'description': self.description,
            'uploader': self.uploader.username if self.uploader else '',
            'play_count': self.play_count,
            'favorite_count': self.favorite_count,
            'comment_count': self.comment_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
        }

    def __repr__(self):
        return f'<Song {self.title} - {self.artist}>'


class Favorite(db.Model):
    """收藏表 — 用户与歌曲的多对多收藏关系"""
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 联合唯一索引 — 同一用户不能重复收藏同一首歌
    __table_args__ = (
        db.UniqueConstraint('user_id', 'song_id', name='uq_user_song_favorite'),
    )

    def __repr__(self):
        return f'<Favorite user={self.user_id} song={self.song_id}>'
