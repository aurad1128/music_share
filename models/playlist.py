"""
歌单模型 (Playlist + PlaylistSong)
支持用户创建个人歌单，管理歌曲收藏
"""
from datetime import datetime
from app import db


class Playlist(db.Model):
    """歌单表 — 用户创建的音乐合集"""
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 歌单中的歌曲（多对多关系）
    songs = db.relationship('PlaylistSong', backref='playlist', lazy='dynamic',
                            cascade='all, delete-orphan',
                            order_by='PlaylistSong.added_at.desc()')

    def song_count(self):
        """返回歌单中歌曲数量"""
        return self.songs.count()

    def __repr__(self):
        return f'<Playlist {self.name}>'


class PlaylistSong(db.Model):
    """歌单-歌曲关联表 — 多对多中间表"""
    __tablename__ = 'playlist_songs'

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联到 Song 模型
    song_info = db.relationship('Song', backref='playlist_entries', lazy=True)

    # 联合唯一索引
    __table_args__ = (
        db.UniqueConstraint('playlist_id', 'song_id', name='uq_playlist_song'),
    )

    def __repr__(self):
        return f'<PlaylistSong playlist={self.playlist_id} song={self.song_id}>'
