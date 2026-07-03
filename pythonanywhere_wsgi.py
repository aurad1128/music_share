"""
PythonAnywhere WSGI 配置 — 把下面内容复制到 Web 控制台的 WSGI 文件中
"""
import sys
import os

# PythonAnywhere 项目路径
project_home = '/home/YOUR_USERNAME/music_share'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application

# 确保 uploads 目录存在
os.makedirs(os.path.join(project_home, 'static', 'uploads', 'covers'), exist_ok=True)
os.makedirs(os.path.join(project_home, 'static', 'uploads', 'avatars'), exist_ok=True)
os.makedirs(os.path.join(project_home, 'static', 'uploads', 'backgrounds'), exist_ok=True)
