"""
选课系统 - Flask 主应用入口
启动方式: python app.py
"""

from flask import Flask, send_from_directory, g
from flask_cors import CORS
from config import Config
import os

from database import get_db, init_db, close_db

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)
CORS(app)


# ============================================================
# 数据库初始化辅助函数
# ============================================================

app.teardown_appcontext

# ============================================================
# 注册蓝图路由
# ============================================================

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.college_admin import college_admin_bp
from routes.teacher import teacher_bp
from routes.student import student_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(college_admin_bp, url_prefix='/api/college-admin')
app.register_blueprint(teacher_bp, url_prefix='/api/teacher')
app.register_blueprint(student_bp, url_prefix='/api/student')


# ============================================================
# 前端页面路由
# ============================================================

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory(os.path.join(app.static_folder, 'pages'), filename)


# ============================================================
# 静态文件服务（CSS, JS, 上传文件等）
# ============================================================

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # 首次启动自动建表
    with app.app_context():
        init_db()
    app.run(debug=True, port=5000)

