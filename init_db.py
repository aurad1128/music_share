"""
数据库初始化脚本 — 创建测试数据
运行方式：python init_db.py  (必须用 Python 3.12)
"""
from app import app, db
from models.user import User
from models.song import Song, Favorite
from models.comment import Comment

with app.app_context():
    # 清除所有表并重建
    db.drop_all()
    db.create_all()
    print('[OK] 数据库表已创建。')

    # ========== 创建测试用户 ==========
    admin = User(
        username='admin',
        email='admin@music.com',
        role='admin',
        bio='系统管理员，负责维护音乐分享平台的正常运营。'
    )
    admin.set_password('admin123')

    user1 = User(
        username='音乐爱好者',
        email='musicfan@example.com',
        role='user',
        bio='热爱音乐，喜欢发现新的声音。'
    )
    user1.set_password('123456')

    user2 = User(
        username='摇滚青年',
        email='rocker@example.com',
        role='user',
        bio='摇滚不死，金属永恒！'
    )
    user2.set_password('123456')

    user3 = User(
        username='古典乐迷',
        email='classical@example.com',
        role='user',
        bio='痴迷于古典音乐的深邃与优雅。'
    )
    user3.set_password('123456')

    db.session.add_all([admin, user1, user2, user3])
    db.session.commit()
    print(f'[OK] 测试用户已创建：admin(管理员), {user1.username}, {user2.username}, {user3.username}')

    # ========== 创建测试歌曲 ==========
    test_songs = [
        Song(title='晴天', artist='周杰伦', album='叶惠美',
             style='流行', description='周杰伦经典作品，校园民谣风格。',
             audio_url='https://music.163.com/outchain/player?type=2&id=186016&auto=0&height=430',
             uploader_id=user1.id, play_count=1520, favorite_count=89, comment_count=23),
        Song(title='夜曲', artist='周杰伦', album='十一月的萧邦',
             style='流行', description='一响起就让人沉醉的旋律。',
             uploader_id=user1.id, play_count=980, favorite_count=67, comment_count=15),
        Song(title='起风了', artist='买辣椒也用券', album='',
             style='流行', description='治愈系流行歌曲，旋律优美。',
             uploader_id=user2.id, play_count=2100, favorite_count=120, comment_count=45),
        Song(title='光年之外', artist='邓紫棋', album='',
             style='流行', description='电影《太空旅客》中文主题曲。',
             uploader_id=user1.id, play_count=1800, favorite_count=95, comment_count=30),
        Song(title='再见杰克', artist='痛仰乐队', album='不要停止我的音乐',
             style='摇滚', description='中国摇滚经典，旋律抓耳。',
             uploader_id=user2.id, play_count=780, favorite_count=56, comment_count=18),
        Song(title='Bohemian Rhapsody', artist='Queen', album='A Night at the Opera',
             style='摇滚', description='摇滚史上最伟大的作品之一。',
             uploader_id=user2.id, play_count=650, favorite_count=42, comment_count=10),
        Song(title='经济舱', artist='Kafe.Hu / KEY.L刘聪', album='',
             style='说唱', description='中文说唱优秀作品，有深度的歌词。',
             uploader_id=user1.id, play_count=560, favorite_count=34, comment_count=12),
        Song(title='Lose Yourself', artist='Eminem', album='8 Mile Soundtrack',
             style='说唱', description='经典说唱，奥斯卡最佳原创歌曲。',
             uploader_id=user3.id, play_count=430, favorite_count=28, comment_count=8),
        Song(title='Faded', artist='Alan Walker', album='Different World',
             style='电子', description='挪威电子音乐制作人的成名作，全球播放量超30亿。',
             audio_url='https://music.163.com/outchain/player?type=2&id=36990266&auto=0&height=430',
             uploader_id=user1.id, play_count=3200, favorite_count=156, comment_count=52),
        Song(title='Waiting For Love', artist='Avicii', album='Stories',
             style='电子', description='瑞典电音天才Avicii的经典。',
             uploader_id=user2.id, play_count=2700, favorite_count=130, comment_count=40),
        Song(title='月光奏鸣曲', artist='贝多芬', album='',
             style='古典', description='贝多芬第十四号钢琴奏鸣曲，永恒的经典。',
             uploader_id=user3.id, play_count=340, favorite_count=25, comment_count=6),
        Song(title='四季·春', artist='维瓦尔第', album='四季',
             style='古典', description='巴洛克时期最著名的音乐作品之一。',
             uploader_id=user3.id, play_count=290, favorite_count=20, comment_count=5),
    ]
    for song in test_songs:
        db.session.add(song)
    db.session.commit()
    print(f'[OK] {len(test_songs)} 首测试歌曲已添加。')

    # ========== 创建测试收藏 ==========
    test_favorites = [
        Favorite(user_id=user1.id, song_id=5),
        Favorite(user_id=user1.id, song_id=3),
        Favorite(user_id=user2.id, song_id=1),
        Favorite(user_id=user2.id, song_id=6),
        Favorite(user_id=user3.id, song_id=11),
        Favorite(user_id=user3.id, song_id=12),
    ]
    for fav in test_favorites:
        db.session.add(fav)
    db.session.commit()
    print(f'[OK] {len(test_favorites)} 条收藏记录已添加。')

    # ========== 创建测试评论 ==========
    test_comments = [
        Comment(user_id=user2.id, song_id=1, content='周杰伦YYDS！这首歌听了十几年了还是那么好听。'),
        Comment(user_id=user3.id, song_id=1, content='每次听都有不同的感受，这就是经典的魅力。'),
        Comment(user_id=user1.id, song_id=5, content='痛仰的现场太炸了！'),
        Comment(user_id=user3.id, song_id=9, content='Alan Walker的电子音乐很有辨识度。'),
        Comment(user_id=user2.id, song_id=11, content='贝多芬永远是最伟大的音乐家之一。'),
        Comment(user_id=user1.id, song_id=12, content='维瓦尔第的四季让人心情愉悦。'),
    ]
    for comment in test_comments:
        db.session.add(comment)
    db.session.commit()
    print(f'[OK] {len(test_comments)} 条评论已添加。')

    print('')
    print('=' * 50)
    print('  测试账号：')
    print('  管理员 - 用户名: admin     密码: admin123')
    print('  用户1  - 用户名: 音乐爱好者  密码: 123456')
    print('  用户2  - 用户名: 摇滚青年   密码: 123456')
    print('  用户3  - 用户名: 古典乐迷   密码: 123456')
    print('=' * 50)
