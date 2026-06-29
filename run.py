"""
音乐分享与推荐网站 — 启动入口
题目二十四：音乐分享与推荐网站

启动方式: python run.py  (必须用 Python 3.12)
"""
from app import app
from waitress import serve
import sys

if __name__ == '__main__':
    print('=' * 50)
    print('  音乐分享与推荐网站 -- 乐享')
    print('  访问地址: http://127.0.0.1:5000')
    print('  测试账号: admin / admin123')
    print('  按 Ctrl+C 停止服务器')
    print('=' * 50)
    sys.stdout.flush()
    serve(app, host='127.0.0.1', port=5000)
