# PythonAnywhere 部署指南

## 第一步：注册账号

1. 打开 https://www.pythonanywhere.com
2. 点 "Start running Python online" → "Create a Beginner account"（免费）
3. 注册完成后登录

---

## 第二步：上传项目

### 方式一：Git 克隆（推荐，梯子开着）
在 PythonAnywhere 的 **Consoles** 标签页 → 打开一个 **Bash** 终端：

```bash
git clone https://github.com/aurad1128/music_share.git
```

### 方式二：手动上传
1. PythonAnywhere → **Files** 标签页
2. 进入 `/home/你的用户名/` 目录
3. 点 "Upload a file"，把 `music_share` 文件夹里的所有文件逐个上传（比较慢，推荐方式一）

---

## 第三步：安装依赖

在 **Bash** 终端中：

```bash
cd ~/music_share
pip install --user -r requirements.txt
```

---

## 第四步：创建 Web 应用

1. PythonAnywhere → **Web** 标签页
2. 点 "Add a new web app"
3. 选择 **Flask** 框架
4. 选择 **Python 3.10** 版本
5. 路径填：`/home/你的用户名/music_share`

---

## 第五步：配置 WSGI 文件

1. **Web** 标签页 → 找到 "Code" 区域的 WSGI 配置文件链接（蓝色链接）
2. 点击打开，**全部删除**，粘贴以下内容：

```python
import sys
import os

project_home = '/home/你的用户名/music_share'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.makedirs(os.path.join(project_home, 'static', 'uploads', 'covers'), exist_ok=True)
os.makedirs(os.path.join(project_home, 'static', 'uploads', 'avatars'), exist_ok=True)
os.makedirs(os.path.join(project_home, 'static', 'uploads', 'backgrounds'), exist_ok=True)

from app import app as application
```

3. **把"你的用户名"改成你实际的 PythonAnywhere 用户名**
4. 保存

---

## 第六步：配置静态文件

在 **Web** 标签页 "Static files" 区域：

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/你的用户名/music_share/static/` |

---

## 第七步：重新加载

点 **Web** 标签页顶部的大绿色按钮 **"Reload"**。

然后在浏览器打开：`https://你的用户名.pythonanywhere.com`

---

## ⚠️ 注意事项

- **免费账号**：有出站网络限制，B站视频播放器可以正常加载（浏览器端请求）
- **数据库**：如果 gitz clone 下载了 `music_share.db`，所有歌曲和用户数据都会保留
- **封面图片**：`static/uploads/covers/` 下的 13 个封面文件会自动随 Git 上传
- **域名**：免费版是 `你的用户名.pythonanywhere.com`

---

## 如果网站打不开

在 **Web** 标签页查看 "Error log" 链接，看看报什么错。
