"""
关注关系模型 (Follow)
多对多自引用关系，记录用户之间的关注
"""
from datetime import datetime
from app import db


class Follow(db.Model):
    """关注表 — 记录用户之间的关注关系"""
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 联合唯一索引：同一对用户不能重复关注
    __table_args__ = (
        db.UniqueConstraint('follower_id', 'followed_id', name='uq_follow'),
    )

    # 关系
    follower = db.relationship('User', foreign_keys=[follower_id],
                               backref=db.backref('following_rels', lazy='dynamic',
                                                  cascade='all, delete-orphan'))
    followed = db.relationship('User', foreign_keys=[followed_id],
                               backref=db.backref('follower_rels', lazy='dynamic',
                                                  cascade='all, delete-orphan'))
