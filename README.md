# 🎵 乐享 — 音乐分享与推荐网站

**Python 程序设计课程设计 · 题目二十四 · 智科 2401-2 · 项目已完成**

---

## 项目状态

✅ **P1 + P2 全部完成** — 2026年6月

---

## 一、功能清单

### 核心功能
- 用户注册/登录/登出 + 多角色权限（user/admin）
- 音乐上传（含封面）/编辑/删除
- 9种风格分类浏览 + 模糊搜索
- B站视频嵌入播放（13首测试歌曲）
- 官方专辑封面（iTunes + 网易云音乐）
- 收藏（AJAX无刷新）/ 评论 / 歌单CRUD
- 排行榜（收藏/评论/播放 三维度 + 本周/本月/全部时间筛选）
- 基于浏览记录的推荐引擎
- 用户个人主页 + 资料编辑 + 头像上传

### 社交功能
- 关注/取关（AJAX）
- 粉丝列表 / 关注列表
- 首页关注动态

### 管理后台
- 仪表盘（用户/歌曲/评论/收藏/播放统计）
- 用户管理（角色切换/删除）
- 歌曲管理（强制删除）
- Chart.js 数据可视化图表

### 皮肤系统
- 6种图标颜色 × 3种背景颜色 = 18种组合
- 自定义背景图片上传 + 模糊度调节
- 设置自动保存，刷新不丢

---

## 二、技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Flask + Flask-SQLAlchemy + Flask-Login |
| 数据库 | SQLite（7张表） |
| 前端 | HTML5 + CSS3 + Bootstrap 5 + Chart.js（CDN） |
| 图标 | Font Awesome 6（CDN） |
| WSGI | Waitress |
| Python | 3.10+ |

---

## 三、快速启动

```bash
# 1. 进入项目目录
cd C:\Users\12692\Desktop\music_share

# 2. 安装依赖（首次）
pip install -r requirements.txt

# 3. 启动
python run.py

# 4. 浏览器打开
http://127.0.0.1:5000
```

---

## 四、测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | `admin` | `admin123` |
| 普通用户 | `音乐爱好者` | `123456` |
| 普通用户 | `摇滚青年` | `123456` |
| 普通用户 | `古典乐迷` | `123456` |

---

## 五、项目目录

```
music_share/
├── run.py                    # 启动入口
├── app.py                    # Flask 应用
├── config.py                 # 配置
├── requirements.txt          # 依赖
├── 网络配置指南.txt           # 局域网/公网访问配置
├── models/                   # 数据模型（7张表）
├── controllers/              # 控制器（7个蓝图）
├── templates/                # 视图模板（20+页面）
├── static/                   # CSS/JS/上传文件
└── utils/                    # 工具函数
```

---

## 六、数据库（7张表）

User / Song / Favorite / Playlist / PlaylistSong / Comment / BrowseRecord / Follow

---

## 七、网络访问

- **本机**：http://127.0.0.1:5000
- **局域网**：需开放防火墙5000端口，详见 `网络配置指南.txt`
- **答辩演示**：直接用本机地址即可

---

## 八、GitHub

https://github.com/aurad1128/music_share
