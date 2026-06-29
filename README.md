# 🎵 乐享 — 音乐分享与推荐网站

**Python 程序设计课程设计 · 题目二十四 · 智科 2401-2**

---

## 一、项目概述

基于 Flask + SQLite + Bootstrap 5 构建的音乐分享与推荐 Web 应用。支持用户上传音乐作品、按风格分类浏览、音乐搜索、管理员后台等核心功能。采用 MVC 架构，实现多角色权限管理（普通用户 / 管理员）。

## 二、技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | Flask | 3.1+ |
| ORM | Flask-SQLAlchemy | 3.1+ |
| 数据库 | SQLite | — |
| 用户认证 | Flask-Login + Werkzeug 哈希 | 0.6+ |
| 前端 | HTML5 + CSS3 + Bootstrap 5 (CDN) | 5.3 |
| 图标 | Font Awesome 6 (CDN) | 6.4 |
| WSGI 服务器 | Waitress | — |
| Python | **3.12**（必须，不要用 3.14 alpha） | 3.12.7 |

## 三、快速启动

### 1. 安装依赖
```bash
cd C:\Users\WZY18\Desktop\music_share
C:\Users\WZY18\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt
```

### 2. 初始化数据库（已有测试数据可跳过）
```bash
C:\Users\WZY18\AppData\Local\Programs\Python\Python312\python.exe init_db.py
```

### 3. 启动应用
```bash
C:\Users\WZY18\AppData\Local\Programs\Python\Python312\python.exe run.py
```

### 4. 打开浏览器访问
```
http://127.0.0.1:5000
```

> ⚠️ **重要**：必须用 `run.py` 启动（不是 `app.py`），必须用 Python 3.12！

## 四、测试账号

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | `admin` | `admin123` | 可访问后台 `/admin/` |
| 普通用户 | `音乐爱好者` | `123456` | 已上传多首歌曲 |
| 普通用户 | `摇滚青年` | `123456` | 摇滚风格爱好者 |
| 普通用户 | `古典乐迷` | `123456` | 古典风格爱好者 |

## 五、项目目录结构

```
music_share/
├── run.py                     # ✅ 启动入口（必须用这个！）
├── app.py                     # Flask 应用主文件（不要直接运行）
├── config.py                  # 配置文件
├── requirements.txt           # 依赖列表
├── init_db.py                 # 数据库初始化 + 测试数据
├── README.md                  # 本文件
│
├── models/                    # 数据模型层 (M)
│   ├── user.py                # 用户模型（含角色：user/admin）
│   ├── song.py                # 歌曲模型 + 收藏模型
│   ├── playlist.py            # 歌单模型 + 歌单-歌曲关联
│   ├── comment.py             # 评论模型
│   └── browse_record.py       # 浏览记录模型（推荐算法用）
│
├── controllers/               # 控制器层 (C)
│   ├── auth.py                # 注册 / 登录 / 登出
│   ├── main.py                # 首页 / 风格浏览 / 搜索 / 用户主页
│   ├── song.py                # 歌曲上传 / 详情 / 编辑 / 删除 / 收藏
│   ├── admin.py               # 管理员后台（仪表盘/用户管理/歌曲管理）
│   ├── playlist.py            # 歌单 CRUD + 添加/移除歌曲
│   └── comment.py             # 评论发表 / 删除
│
├── templates/                 # 视图层 (V) — Jinja2 模板
│   ├── base.html              # 基础布局（导航栏+页脚+CDN引用）
│   ├── index.html             # 首页（最新歌曲+热门排行+全部歌曲）
│   ├── auth/
│   │   ├── login.html         # 登录页
│   │   └── register.html      # 注册页
│   ├── songs/
│   │   ├── browse.html        # 风格分类浏览
│   │   ├── detail.html        # 歌曲详情（播放+评论+推荐）
│   │   ├── upload.html        # 上传音乐
│   │   ├── edit.html          # 编辑歌曲
│   │   └── search.html        # 搜索结果
│   ├── user/
│   │   └── profile.html       # 用户个人音乐主页
│   ├── admin/
│   │   ├── dashboard.html     # 管理仪表盘
│   │   ├── users.html         # 用户管理列表
│   │   └── songs.html         # 歌曲管理列表
│   └── playlists/
│       ├── my.html            # 我的歌单列表
│       ├── create.html        # 创建歌单
│       ├── detail.html        # 歌单详情
│       └── edit.html          # 编辑歌单
│
├── static/                    # 静态资源
│   ├── css/style.css          # 自定义暗色音乐主题样式
│   ├── js/main.js             # 收藏AJAX、图片预览、消息自动关闭
│   └── uploads/covers/        # 专辑封面上传目录
│
└── utils/
    └── decorators.py          # @admin_required 权限装饰器
```

## 六、数据库设计（6 张表）

### User（用户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| username | String(80) UNIQUE | 用户名 |
| email | String(120) UNIQUE | 邮箱 |
| password_hash | String(256) | Werkzeug 哈希密码 |
| avatar | String(256) | 头像路径 |
| bio | Text | 个人简介 |
| role | String(20) default='user' | user / admin |
| created_at | DateTime | 注册时间 |

### Song（歌曲表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| title | String(200) | 歌曲名称 |
| artist | String(200) | 歌手名 |
| album | String(200) | 专辑名 |
| cover_image | String(500) | 封面图文件名 |
| audio_url | String(500) | 音频/视频嵌入链接 |
| style | String(50) | 风格（流行/摇滚/说唱/电子/古典/民谣/爵士/R&B/其他） |
| description | Text | 歌曲简介 |
| uploader_id | FK→User.id | 上传者 |
| play_count | Integer | 播放次数（排行榜用） |
| favorite_count | Integer | 收藏数（排行榜用） |
| comment_count | Integer | 评论数（排行榜用） |
| created_at | DateTime | 上传时间 |

### Favorite（收藏表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | |
| user_id | FK→User.id | 联合唯一索引 |
| song_id | FK→Song.id | 联合唯一索引 |
| created_at | DateTime | |

### Playlist（歌单表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | |
| name | String(200) | 歌单名 |
| description | Text | 描述 |
| user_id | FK→User.id | 创建者 |
| is_public | Boolean | 是否公开 |
| created_at | DateTime | |

### PlaylistSong（歌单-歌曲关联表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | |
| playlist_id | FK→Playlist.id | 联合唯一索引 |
| song_id | FK→Song.id | 联合唯一索引 |
| added_at | DateTime | |

### Comment（评论表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | |
| user_id | FK→User.id | |
| song_id | FK→Song.id | |
| content | Text | 评论内容 |
| created_at | DateTime | |

## 七、路由总览

### 公开路由
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 首页（最新歌曲+热门排行） |
| GET | `/login` | 登录页 |
| POST | `/login` | 提交登录 |
| GET | `/register` | 注册页 |
| POST | `/register` | 提交注册 |
| GET | `/browse` | 风格总览 |
| GET | `/browse/<style>` | 按风格浏览（如 `/browse/流行`） |
| GET | `/search?q=` | 按歌名/歌手搜索 |
| GET | `/song/<id>` | 歌曲详情页 |
| GET | `/user/<id>` | 用户个人主页 |

### 需登录路由
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/logout` | 退出登录 |
| GET/POST | `/song/upload` | 上传音乐 |
| GET/POST | `/song/<id>/edit` | 编辑自己的歌曲 |
| POST | `/song/<id>/delete` | 删除自己的歌曲 |
| POST | `/song/<id>/favorite` | 收藏/取消（AJAX） |
| GET/POST | `/playlist/create` | 创建歌单 |
| GET/POST | `/playlist/<id>/edit` | 编辑歌单 |
| POST | `/playlist/<id>/delete` | 删除歌单 |
| POST | `/playlist/<id>/add_song/<song_id>` | 向歌单添加歌曲 |
| POST | `/playlist/<id>/remove_song/<song_id>` | 从歌单移除歌曲 |
| POST | `/comment/song/<id>` | 发表评论 |
| POST | `/comment/<id>/delete` | 删除自己的评论 |

### 管理员专属路由（需 admin 角色）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/` | 管理仪表盘 |
| GET | `/admin/users` | 用户管理 |
| POST | `/admin/user/<id>/toggle` | 切换用户角色 |
| POST | `/admin/user/<id>/delete` | 删除用户 |
| GET | `/admin/songs` | 歌曲管理 |
| POST | `/admin/song/<id>/delete` | 强制删除任意歌曲 |

## 八、权限矩阵

| 操作 | 未登录 | 普通用户 | 管理员 |
|------|--------|----------|--------|
| 浏览/搜索歌曲 | ✅ | ✅ | ✅ |
| 注册/登录 | ✅ | — | — |
| 上传歌曲 | ❌ | ✅ | ✅ |
| 编辑/删除自己的歌曲 | ❌ | ✅ | ✅ |
| 收藏歌曲 | ❌ | ✅ | ✅ |
| 创建/管理歌单 | ❌ | ✅ | ✅ |
| 发表/删除自己的评论 | ❌ | ✅ | ✅ |
| 删除任意歌曲 | ❌ | ❌ | ✅ |
| 管理用户（角色/删除） | ❌ | ❌ | ✅ |
| 访问 `/admin/` | ❌ (403) | ❌ (403) | ✅ |

## 九、开发进度

### ✅ P1 已完成（地基+核心）
- [x] 项目架构搭建（MVC + 蓝图）
- [x] 6张数据表模型设计
- [x] 用户注册/登录/登出（含中文用户名支持）
- [x] 密码哈希安全存储
- [x] 多角色权限体系（普通用户 + 管理员）
- [x] 权限装饰器（@admin_required）
- [x] 歌曲上传（含专辑封面上传）
- [x] 按风格分类浏览（9种风格）
- [x] 音乐搜索（歌名/歌手模糊匹配）
- [x] 歌曲详情页（含同风格推荐）
- [x] 歌曲编辑/删除（权限验证）
- [x] 管理员仪表盘（4项统计数据）
- [x] 管理员用户管理（角色切换/删除）
- [x] 管理员歌曲管理（强制删除）
- [x] 暗色音乐主题 UI（响应式）
- [x] 歌单创建/编辑/删除
- [x] 评论发表/删除
- [x] 收藏/取消收藏（AJAX）
- [x] 用户个人音乐主页
- [x] 测试数据（4用户 + 12首歌 + 6评论 + 6收藏）

### 🔵 P2 待完成（第二位组员）
- [ ] **播放器嵌入优化**：目前 iframe 嵌入已实现，可增强为内嵌播放器
- [ ] **排行榜自动生成**：Song 表已有 `play_count/favorite_count/comment_count` 字段，首页已有 TOP10 预览，需完善排行榜独立页面（按三种维度排名切换）
- [ ] **猜你喜欢推荐**：BrowseRecord 表已建好，记录浏览行为。算法思路：统计用户浏览最多的风格 → 推荐该风格下未听过的高收藏歌曲
- [ ] **个人主页增强**：路由+模板已写，可增加编辑个人资料（修改简介/头像）
- [ ] **歌单添加功能**：后端已写好，前端需在歌曲详情页加上"添加到歌单"的下拉菜单
- [ ] **社交功能扩展**：关注用户、分享歌曲链接等
- [ ] **数据可视化**：管理后台增加图表（Chart.js）

## 十、开发注意事项

1. **必须用 Python 3.12**：`C:\Users\WZY18\AppData\Local\Programs\Python\Python312\python.exe`
2. **必须用 run.py 启动**：不要 `python app.py`（会导致双导入问题）
3. **代码风格**：PEP8，关键函数有中文注释
4. **数据库**：SQLite 文件在项目根目录 `music_share.db`，删除后运行 `init_db.py` 即可重建
5. **模板使用**：所有页面继承 `base.html`，使用 Jinja2 语法
6. **表单验证**：目前是手动验证，如需更强验证可引入 Flask-WTF 的 `form.validate_on_submit()`
7. **前端框架**：Bootstrap 5 通过 CDN 引入，无需本地文件
