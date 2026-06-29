"""
主页/浏览/搜索控制器 — 音乐发现的核心入口
- 首页：猜你喜欢 + 最新歌曲 + 热门排行
- 风格浏览：按流行/摇滚/说唱/电子/古典等分类
- 搜索：按歌名/歌手名模糊搜索
- 排行榜：按收藏/评论/播放三维度排名
- 用户主页：个人资料/上传作品/歌单
"""
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models.song import Song
from models.user import User
from models.playlist import Playlist
from models.browse_record import BrowseRecord
from models.follow import Follow
from app import db
from config import Config

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页 — 猜你喜欢 + 最新上传 + 热门排行"""
    page = request.args.get('page', 1, type=int)

    # 猜你喜欢推荐
    recommended = []
    if current_user.is_authenticated:
        records = BrowseRecord.query.filter_by(
            user_id=current_user.id
        ).order_by(BrowseRecord.browse_count.desc()).limit(20).all()

        if records:
            # 统计用户最常浏览的风格
            style_scores = {}
            for rec in records:
                if rec.song:
                    s = rec.song.style
                    style_scores[s] = style_scores.get(s, 0) + rec.browse_count
            top_style = max(style_scores, key=style_scores.get)

            # 推荐该风格下用户未浏览过的热门歌曲
            browsed_ids = [r.song_id for r in records]
            recommended = Song.query.filter(
                Song.style == top_style,
                ~Song.id.in_(browsed_ids)
            ).order_by(Song.favorite_count.desc()).limit(6).all()
        else:
            # 新用户：推荐全站最热歌曲
            recommended = Song.query.order_by(
                Song.favorite_count.desc()).limit(6).all()

    # 关注动态（登录用户可见）
    feed_songs = []
    if current_user.is_authenticated:
        followed_ids = [f.followed_id for f in
                        Follow.query.filter_by(follower_id=current_user.id).all()]
        if followed_ids:
            feed_songs = Song.query.filter(
                Song.uploader_id.in_(followed_ids)
            ).order_by(Song.created_at.desc()).limit(6).all()

    # 最新上传
    latest_songs = Song.query.order_by(Song.created_at.desc()).limit(6).all()
    # 热门排行
    hot_songs = Song.query.order_by(Song.favorite_count.desc()).limit(10).all()
    # 全部歌曲分页
    all_songs = Song.query.order_by(Song.created_at.desc()).paginate(
        page=page, per_page=Config.SONGS_PER_PAGE, error_out=False)

    return render_template('index.html',
                         recommended=recommended,
                         feed_songs=feed_songs,
                         latest_songs=latest_songs,
                         hot_songs=hot_songs,
                         all_songs=all_songs,
                         styles=Config.MUSIC_STYLES)


@main_bp.route('/browse')
def browse():
    """风格总览页 — 展示所有风格分类入口及歌曲数量"""
    style_data = []
    for style in Config.MUSIC_STYLES:
        count = Song.query.filter_by(style=style).count()
        style_data.append({'name': style, 'count': count})
    return render_template('songs/browse.html', styles=Config.MUSIC_STYLES, style_data=style_data)


@main_bp.route('/browse/<style>')
def browse_by_style(style):
    """按风格分类浏览歌曲"""
    page = request.args.get('page', 1, type=int)
    if style not in Config.MUSIC_STYLES:
        style = '其他'

    songs = Song.query.filter_by(style=style).order_by(
        Song.created_at.desc()).paginate(
        page=page, per_page=Config.SONGS_PER_PAGE, error_out=False)

    return render_template('songs/browse.html',
                         songs=songs,
                         current_style=style,
                         styles=Config.MUSIC_STYLES,
                         style_data=None)


@main_bp.route('/search')
def search():
    """音乐搜索 — 按歌名/歌手名模糊搜索"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    if not query:
        return render_template('songs/search.html', songs=None, query='',
                             total_count=Song.query.count())

    search_pattern = f'%{query}%'
    songs = Song.query.filter(
        (Song.title.like(search_pattern)) | (Song.artist.like(search_pattern))
    ).order_by(Song.created_at.desc()).paginate(
        page=page, per_page=Config.SONGS_PER_PAGE, error_out=False)

    return render_template('songs/search.html', songs=songs, query=query)


@main_bp.route('/ranking')
def ranking():
    """音乐排行榜 — 按收藏数/评论数/播放数排名，支持时间筛选"""
    from datetime import datetime, timedelta

    sort_by = request.args.get('sort', 'favorites')
    period = request.args.get('period', 'all')
    page = request.args.get('page', 1, type=int)

    sort_field = {
        'favorites': Song.favorite_count,
        'comments': Song.comment_count,
        'plays': Song.play_count,
    }.get(sort_by, Song.favorite_count)

    # 构建基础查询
    query = Song.query

    # 时间筛选
    now = datetime.utcnow()
    if period == 'week':
        week_ago = now - timedelta(days=7)
        query = query.filter(Song.created_at >= week_ago)
    elif period == 'month':
        month_ago = now - timedelta(days=30)
        query = query.filter(Song.created_at >= month_ago)

    songs = query.order_by(sort_field.desc()).paginate(
        page=page, per_page=20, error_out=False)

    return render_template('songs/ranking.html', songs=songs,
                         sort_by=sort_by, period=period)


@main_bp.route('/user/<int:user_id>')
def user_profile(user_id):
    """用户个人音乐主页"""
    profile_user = User.query.get_or_404(user_id)
    songs = Song.query.filter_by(uploader_id=user_id).order_by(
        Song.created_at.desc()).limit(12).all()
    playlists = Playlist.query.filter_by(user_id=user_id).order_by(
        Playlist.created_at.desc()).all()

    # 关注统计
    follower_count = Follow.query.filter_by(followed_id=user_id).count()
    following_count = Follow.query.filter_by(follower_id=user_id).count()
    is_following = False
    if current_user.is_authenticated and current_user.id != user_id:
        is_following = Follow.query.filter_by(
            follower_id=current_user.id, followed_id=user_id).first() is not None

    return render_template('user/profile.html',
                         profile_user=profile_user,
                         songs=songs,
                         playlists=playlists,
                         follower_count=follower_count,
                         following_count=following_count,
                         is_following=is_following)


@main_bp.route('/user/<int:user_id>/following')
def user_following(user_id):
    """查看用户关注的人"""
    profile_user = User.query.get_or_404(user_id)
    follows = Follow.query.filter_by(follower_id=user_id).order_by(
        Follow.created_at.desc()).all()
    return render_template('user/follow_list.html',
                         profile_user=profile_user,
                         users=[f.followed for f in follows],
                         list_type='following')


@main_bp.route('/user/<int:user_id>/followers')
def user_followers(user_id):
    """查看用户的粉丝"""
    profile_user = User.query.get_or_404(user_id)
    followers = Follow.query.filter_by(followed_id=user_id).order_by(
        Follow.created_at.desc()).all()
    return render_template('user/follow_list.html',
                         profile_user=profile_user,
                         users=[f.follower for f in followers],
                         list_type='followers')


@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑个人资料 — 修改简介 / 上传头像"""
    if request.method == 'POST':
        bio = request.form.get('bio', '').strip()
        current_user.bio = bio

        # 处理头像上传
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and avatar_file.filename:
                save_cover = current_app.config.get('save_cover')
                if save_cover:
                    avatar_dir = os.path.join(
                        current_app.config['UPLOADED_COVERS_DEST'].replace('covers', 'avatars'))
                    os.makedirs(avatar_dir, exist_ok=True)
                    result = save_cover(avatar_file, avatar_dir)
                    if result:
                        # 删除旧头像
                        if current_user.avatar and current_user.avatar != 'default_avatar.png':
                            old_path = os.path.join(avatar_dir, current_user.avatar)
                            if os.path.exists(old_path):
                                os.remove(old_path)
                        current_user.avatar = result

        db.session.commit()
        flash('个人资料更新成功！', 'success')
        return redirect(url_for('main.user_profile', user_id=current_user.id))

    return render_template('user/edit_profile.html')


@main_bp.route('/theme', methods=['GET', 'POST'])
@login_required
def theme_settings():
    """皮肤设置 — 选择预设主题 / 自定义背景 / 模糊度"""
    if request.method == 'POST':
        action = request.form.get('action', '')

        if action == 'bg_upload' and 'bg_image' in request.files:
            bg_file = request.files['bg_image']
            if bg_file and bg_file.filename:
                save_cover = current_app.config.get('save_cover')
                if save_cover:
                    bg_dir = os.path.join(
                        current_app.config['UPLOADED_COVERS_DEST'].replace('covers', 'backgrounds'))
                    os.makedirs(bg_dir, exist_ok=True)
                    result = save_cover(bg_file, bg_dir)
                    if result:
                        flash('自定义背景上传成功！', 'success')
                    else:
                        flash('背景上传失败，支持 png/jpg/gif/webp 格式。', 'danger')

        elif action == 'clear_bg':
            flash('自定义背景已清除。', 'info')

        return redirect(url_for('main.theme_settings'))

    # 列出已上传的背景图片
    bg_dir = os.path.join(current_app.config['UPLOADED_COVERS_DEST'].replace('covers', 'backgrounds'))
    os.makedirs(bg_dir, exist_ok=True)
    bg_files = []
    if os.path.exists(bg_dir):
        bg_files = [f for f in os.listdir(bg_dir)
                    if f.rsplit('.', 1)[-1].lower() in ('png', 'jpg', 'jpeg', 'gif', 'webp')]

    return render_template('theme.html', bg_files=bg_files)


@main_bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    """关注/取关用户 — AJAX 请求，返回 JSON"""
    if user_id == current_user.id:
        return {'status': 'error', 'message': '不能关注自己'}, 400

    target = User.query.get_or_404(user_id)
    follow = Follow.query.filter_by(
        follower_id=current_user.id, followed_id=user_id).first()

    if follow:
        db.session.delete(follow)
        db.session.commit()
        follower_count = Follow.query.filter_by(followed_id=user_id).count()
        return {'status': 'unfollowed', 'follower_count': follower_count}
    else:
        follow = Follow(follower_id=current_user.id, followed_id=user_id)
        db.session.add(follow)
        db.session.commit()
        follower_count = Follow.query.filter_by(followed_id=user_id).count()
        return {'status': 'followed', 'follower_count': follower_count}
