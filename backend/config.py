"""
选课系统 - 配置文件
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # TODO: 后续从环境变量读取敏感配置
    SECRET_KEY = 'course-selection-secret-key-change-in-production'
    DATABASE = os.path.join(BASE_DIR, '..', 'database', 'course_selection.db')

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

    # 分页配置
    PAGE_SIZE = 20
