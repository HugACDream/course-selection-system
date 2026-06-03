"""
学生路由
需求8: 根据学号和密码进入选课界面，查询已选课程、指定选修课程、查询基本信息
需求9: 查询自己选课结果
需求10: 选课时检查先修课程，未学习则提示不能选课
需求11: 浏览课程信息和查询成绩，下载课件
需求12: 给任课教师发送信息和回复任课教师的留言
"""

from flask import Blueprint, request, jsonify, session, send_from_directory
import os

student_bp = Blueprint('student', __name__)


def student_required():
    """校验当前用户是否为学生，并返回student_id"""
    # TODO: 从 session 获取当前用户，检查 role == 'student'
    user = session.get('user')
    if not user or user.get('role') != 'student':
        return None, jsonify({'success': False, 'message': '无权限，需要学生登录'}), 403
    return user.get('id'), None, None


# ============================================================
# 个人信息（需求8: 对自己基本信息的查询）
# ============================================================

@student_bp.route('/profile', methods=['GET'])
def get_profile():
    """查询个人信息"""
    # TODO: student_id, err, resp = student_required() → 校验
    # TODO: 调用 User.find_by_id(student_id) 查询个人信息
    return jsonify({'success': False, 'message': 'TODO: 查询个人信息待实现'})


@student_bp.route('/profile', methods=['PUT'])
def update_profile():
    """修改个人信息（如邮箱、电话等）"""
    # TODO: 校验学生权限，更新个人信息
    return jsonify({'success': False, 'message': 'TODO: 修改个人信息待实现'})


# ============================================================
# 课程浏览（需求11: 浏览课程信息）
# ============================================================

@student_bp.route('/courses', methods=['GET'])
def list_courses():
    """浏览所有可选课程列表"""
    # TODO: 校验学生权限
    # TODO: 调用 Course.find_all() 查询所有课程
    # TODO: 返回课程列表，附带选课人数信息
    return jsonify({'success': False, 'message': 'TODO: 浏览课程列表待实现'})


@student_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    """浏览课程详情（含课程介绍、先修课程等）"""
    # TODO: 校验学生权限
    # TODO: 调用 Course.find_by_id(course_id)
    return jsonify({'success': False, 'message': 'TODO: 浏览课程详情待实现'})


# ============================================================
# 选课功能（需求8 & 9 & 10）
# ============================================================

@student_bp.route('/my-selections', methods=['GET'])
def list_my_selections():
    """
    查询已选课程（需求8: 查询已选课程; 需求9: 查询自己选课结果）
    返回: { success, data: [ { selection_id, course_id, course_name, status, ... } ] }
    """
    # TODO: 校验学生权限
    # TODO: 调用 CourseSelection.find_by_student(student_id)
    # TODO: 返回已选课程列表及状态（pending/confirmed/cancelled）
    return jsonify({'success': False, 'message': 'TODO: 查询已选课程待实现'})


@student_bp.route('/select-course', methods=['POST'])
def select_course():
    """
    选择课程（需求8: 指定自己的选修课程）
    请求: { course_id }
    """
    # TODO: student_id, err, resp = student_required() → 校验
    # TODO: 1. 获取 course_id
    # TODO: 2. 调用 Course.find_by_id(course_id) 获取课程信息
    # TODO: 3. 【需求10】检查先修课程:
    #         - 遍历 course.prerequisites
    #         - 查询学生成绩表，检查是否已修完所有先修课程（成绩>=60）
    #         - 如果有先修课未通过，返回错误: "您没有学习该课程的先修课程，不能进行选课！"
    # TODO: 4. 检查是否已选过该课程（防重复）
    # TODO: 5. 创建 CourseSelection 记录，status='pending'
    # TODO: 6. 返回选课结果
    return jsonify({'success': False, 'message': 'TODO: 选课功能待实现'})


@student_bp.route('/cancel-selection/<int:selection_id>', methods=['POST'])
def cancel_selection(selection_id):
    """取消选课"""
    # TODO: 校验学生权限，验证选课记录属于当前学生
    # TODO: 更新状态为 'cancelled'
    return jsonify({'success': False, 'message': 'TODO: 取消选课待实现'})


# ============================================================
# 成绩查询（需求11: 查询成绩）
# ============================================================

@student_bp.route('/my-grades', methods=['GET'])
def list_my_grades():
    """查询我的所有成绩"""
    # TODO: 校验学生权限
    # TODO: 调用 Grade.find_by_student(student_id)
    return jsonify({'success': False, 'message': 'TODO: 查询成绩待实现'})


# ============================================================
# 课件下载（需求11: 下载课件）
# ============================================================

@student_bp.route('/courses/<int:course_id>/download-material', methods=['GET'])
def download_course_material(course_id):
    """下载课程课件"""
    # TODO: 1. 校验学生权限
    # TODO: 2. 验证学生已选中该课程（status='confirmed'）
    # TODO: 3. 获取 course.course_material_path
    # TODO: 4. 返回文件下载
    return jsonify({'success': False, 'message': 'TODO: 下载课件待实现'})


# ============================================================
# 消息功能（需求12: 给任课教师发送信息和回复任课教师的留言）
# ============================================================

@student_bp.route('/messages/send', methods=['POST'])
def send_message():
    """
    给任课教师发送消息（需求12: 给教师发送信息）
    请求: { receiver_id, course_id, content, reply_to? }
    """
    # TODO: student_id, err, resp = student_required() → 校验
    # TODO: 创建 Message 对象，sender_id=student_id，调用 save()
    return jsonify({'success': False, 'message': 'TODO: 发送消息待实现'})


@student_bp.route('/messages/received', methods=['GET'])
def list_received_messages():
    """查询收到的消息列表（含教师的留言）"""
    # TODO: 校验学生权限
    # TODO: 调用 Message.find_received(student_id)
    return jsonify({'success': False, 'message': 'TODO: 查询收件箱待实现'})


@student_bp.route('/messages/sent', methods=['GET'])
def list_sent_messages():
    """查询已发送的消息列表"""
    # TODO: 校验学生权限
    # TODO: 调用 Message.find_sent(student_id)
    return jsonify({'success': False, 'message': 'TODO: 查询发件箱待实现'})


@student_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
def mark_read(message_id):
    """标记消息为已读"""
    # TODO: 校验学生权限，调用 Message.mark_read()
    return jsonify({'success': False, 'message': 'TODO: 标记已读待实现'})


@student_bp.route('/messages/<int:message_id>/reply', methods=['POST'])
def reply_message(message_id):
    """
    回复教师留言（需求12: 回复任课教师的留言）
    请求: { content }
    """
    # TODO: 1. 校验学生权限
    # TODO: 2. 找到原消息，获取 sender_id（教师）和 course_id
    # TODO: 3. 创建新的 Message 记录，receiver_id=原消息的发送者
    # TODO: 4. 设置 reply_to=message_id
    return jsonify({'success': False, 'message': 'TODO: 回复消息待实现'})
