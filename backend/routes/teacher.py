"""
教师路由
需求5: 输入课程介绍、上传课件、发布先修课程、更新和修改课程信息
需求6: 查询中签学生名单，录入成绩，生成成绩统计表
需求7: 对学生发送消息留言
"""

from flask import Blueprint, request, jsonify, session
import os

teacher_bp = Blueprint('teacher', __name__)


def teacher_required():
    """校验当前用户是否为教师，并返回teacher_id"""
    # TODO: 从 session 获取当前用户，检查 role == 'teacher'
    user = session.get('user')
    if not user or user.get('role') != 'teacher':
        return None, jsonify({'success': False, 'message': '无权限，需要教师登录'}), 403
    return user.get('id'), None, None


# ============================================================
# 课程信息管理（需求5: 输入课程介绍、上传课件、发布先修课程、更新和修改课程信息）
# ============================================================

@teacher_bp.route('/courses', methods=['GET'])
def list_my_courses():
    """查询我教授的课程列表"""
    # TODO: teacher_id, err, resp = teacher_required() → 校验
    # TODO: 调用 Course.find_by_teacher(teacher_id)
    return jsonify({'success': False, 'message': 'TODO: 查询我的课程待实现'})


@teacher_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    """查询课程详情"""
    # TODO: 校验教师权限，验证课程属于当前教师
    return jsonify({'success': False, 'message': 'TODO: 查询课程详情待实现'})


@teacher_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    更新课程信息（需求5: 输入课程介绍、发布先修课程、更新和修改课程信息）
    请求: { name, description, credits, syllabus, prerequisites, max_students }
    """
    # TODO: 校验教师权限，验证课程属于当前教师
    # TODO: 获取请求体，更新课程字段
    # TODO: 调用 course.update()
    return jsonify({'success': False, 'message': 'TODO: 更新课程信息待实现'})


@teacher_bp.route('/courses/<int:course_id>/upload-material', methods=['POST'])
def upload_course_material(course_id):
    """
    上传课程课件（需求5: 上传课程的课件）
    请求: multipart/form-data, 文件字段名 'file'
    """
    # TODO: 1. 校验教师权限，验证课程属于当前教师
    # TODO: 2. 从 request.files 获取上传的文件
    # TODO: 3. 保存文件到 UPLOAD_FOLDER/course_{course_id}/ 目录
    # TODO: 4. 更新 Course.course_material_path
    # TODO: 5. 返回文件访问路径
    return jsonify({'success': False, 'message': 'TODO: 上传课件待实现'})


# ============================================================
# 中签学生查询（需求6: 查询选修自己课程的所有中签学生名单）
# ============================================================

@teacher_bp.route('/courses/<int:course_id>/confirmed-students', methods=['GET'])
def get_confirmed_students(course_id):
    """查询某课程的中签学生名单"""
    # TODO: 校验教师权限，验证课程属于当前教师
    # TODO: 调用 CourseSelection.find_confirmed_by_course(course_id)
    # TODO: 返回中签学生列表（含姓名、学号、邮箱等）
    return jsonify({'success': False, 'message': 'TODO: 查询中签学生待实现'})


# ============================================================
# 成绩管理（需求6: 录入课程成绩生成成绩统计表）
# ============================================================

@teacher_bp.route('/courses/<int:course_id>/grades', methods=['GET'])
def list_course_grades(course_id):
    """查询某课程的所有学生成绩"""
    # TODO: 校验教师权限，验证课程属于当前教师
    # TODO: 调用 Grade.find_by_course(course_id)
    return jsonify({'success': False, 'message': 'TODO: 查询课程成绩待实现'})


@teacher_bp.route('/courses/<int:course_id>/grades', methods=['POST'])
def save_grades(course_id):
    """
    批量录入/更新成绩（需求6: 录入课程成绩）
    请求: { grades: [ { student_id, score }, ... ] }
    """
    # TODO: 1. 校验教师权限，验证课程属于当前教师
    # TODO: 2. 遍历 grades 数组，为每个学生创建/更新 Grade 记录
    # TODO: 3. 自动计算 grade_point（如: score >= 90 → 4.0, 80-89 → 3.0 等）
    return jsonify({'success': False, 'message': 'TODO: 录入成绩待实现'})


@teacher_bp.route('/courses/<int:course_id>/statistics', methods=['GET'])
def get_grade_statistics(course_id):
    """
    获取成绩统计表（需求6: 每个分数段的人数、及格率等）
    返回: { avg_score, max_score, min_score, pass_rate, score_distribution: {...} }
    """
    # TODO: 校验教师权限
    # TODO: 调用 Grade.get_statistics(course_id)
    return jsonify({'success': False, 'message': 'TODO: 成绩统计待实现'})


# ============================================================
# 消息功能（需求7: 对选修自己课程学生发送消息留言）
# ============================================================

@teacher_bp.route('/messages/send', methods=['POST'])
def send_message():
    """
    发送消息给学生
    请求: { receiver_id, course_id, content, reply_to? }
    """
    # TODO: teacher_id, err, resp = teacher_required() → 校验
    # TODO: 创建 Message 对象，sender_id=teacher_id，调用 save()
    return jsonify({'success': False, 'message': 'TODO: 发送消息待实现'})


@teacher_bp.route('/messages/received', methods=['GET'])
def list_received_messages():
    """查询收到的消息列表"""
    # TODO: 校验教师权限
    # TODO: 调用 Message.find_received(teacher_id)
    return jsonify({'success': False, 'message': 'TODO: 查询收件箱待实现'})


@teacher_bp.route('/messages/sent', methods=['GET'])
def list_sent_messages():
    """查询已发送的消息列表"""
    # TODO: 校验教师权限
    # TODO: 调用 Message.find_sent(teacher_id)
    return jsonify({'success': False, 'message': 'TODO: 查询发件箱待实现'})


@teacher_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
def mark_read(message_id):
    """标记消息为已读"""
    # TODO: 校验教师权限，调用 Message.mark_read()
    return jsonify({'success': False, 'message': 'TODO: 标记已读待实现'})
