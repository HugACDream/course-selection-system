"""
认证路由 - 登录/登出
"""

from flask import Blueprint, request, jsonify, session
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    请求: { username, password }
    返回: { success, user: { id, username, role, name, college_id } }
    """
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'})

    user = User.find_by_username(username)
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': '用户名或密码错误'})

    session['user'] = user.to_dict()
    return jsonify({'success': True, 'user': user.to_dict()})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    # TODO: 清除 session
    session.clear()
    return jsonify({'success': True, 'message': '已登出'})


@auth_bp.route('/current_user', methods=['GET'])
def current_user():
    """获取当前登录用户信息"""
    user = session.get('user')
    if user:
        return jsonify({'success': True, 'user': user})
    return jsonify({'success': False, 'message': '未登录'})


@auth_bp.route('/change_password', methods=['POST'])
def change_password():
    """修改密码"""
    # TODO: 校验旧密码，更新为新密码
    data = request.get_json()
    return jsonify({'success': False, 'message': 'TODO: 修改密码功能待实现'})
