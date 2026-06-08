"""
学生路由
需求8: 根据学号和密码进入选课界面，查询已选课程、指定选修课程、查询基本信息
需求9: 查询自己选课结果
需求10: 选课时检查先修课程，未学习则提示不能选课
需求11: 浏览课程信息和查询成绩，下载课件
需求12: 给任课教师发送信息和回复任课教师的留言
"""

from flask import Blueprint, request, jsonify, session, send_from_directory
from database import get_db
from models.user import User
from models.course import Course
from models.selection import CourseSelection
from models.grade import Grade
from models.message import Message
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
    student_id, err, resp = student_required()
    if err:
        return resp

    user = User.find_by_id(student_id)
    return jsonify({'success': True, 'user': user.to_dict()})


@student_bp.route('/profile', methods=['PUT'])
def update_profile():
    student_id, err, resp = student_required()
    if err:
        return resp

    user = User.find_by_id(student_id)
    data = request.get_json()
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.update()

    return jsonify({'success': True, 'message': '修改成功', 'user': user.to_dict()})

# ============================================================
# 课程浏览（需求11: 浏览课程信息）
# ============================================================

@student_bp.route('/courses', methods=['GET'])
def list_courses():
    student_id, err, resp = student_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    college_id = request.args.get('college_id', None, type=int)

    courses, total = Course.find_all(college_id=college_id, page=page, page_size=page_size)
    course_list = []
    for c in courses:
        d = c.to_dict()
        d['selection_count'] = Course.get_selection_count(c.id)
        course_list.append(d)

    return jsonify({
        'success': True,
        'data': {'items': course_list, 'total': total, 'page': page, 'page_size': page_size}
    })


@student_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    student_id, err, resp = student_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': '课程不存在'})

    d = course.to_dict()
    d['selection_count'] = Course.get_selection_count(course_id)
    return jsonify({'success': True, 'course': d})

# ============================================================
# 选课功能（需求8 & 9 & 10）
# ============================================================

@student_bp.route('/my-selections', methods=['GET'])
def list_my_selections():
    student_id, err, resp = student_required()
    if err:
        return resp

    items = CourseSelection.find_by_student(student_id)
    return jsonify({'success': True, 'data': items})


@student_bp.route('/select-course', methods=['POST'])
def select_course():
    student_id, err, resp = student_required()
    if err:
        return resp

    data = request.get_json()
    course_id = data.get('course_id')

    if not course_id:
        return jsonify({'success': False, 'message': '课程ID不能为空'})

    course = Course.find_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': '课程不存在'})

    # 需求10：检查先修课程（按课程名称匹配，同名课程修过任一门即可）
    if course.prerequisites:
        db = get_db()
        passed_rows = db.execute(
            'SELECT DISTINCT c.name FROM grades g '
            'JOIN courses c ON g.course_id = c.id '
            'WHERE g.student_id = ? AND g.score >= 60',
            (student_id,)
        ).fetchall()
        passed_names = {r['name'] for r in passed_rows}
        for prereq_name in course.prerequisites:
            if prereq_name not in passed_names:
                return jsonify({
                    'success': False,
                    'message': f'您未修过先修课程"{prereq_name}"，不能选课！'
                })

    # 检查是否已选过
    if CourseSelection.check_exists(student_id, course_id):
        return jsonify({'success': False, 'message': '您已选择过该课程'})

    # 创建选课记录
    selection = CourseSelection()
    selection.student_id = student_id
    selection.course_id = course_id
    selection.status = 'pending'
    selection.save()

    return jsonify({'success': True, 'message': '选课成功，请等待抽签结果', 'data': selection.to_dict()})


@student_bp.route('/cancel-selection/<int:selection_id>', methods=['POST'])
def cancel_selection(selection_id):
    student_id, err, resp = student_required()
    if err:
        return resp

    selection = CourseSelection.find_by_id(selection_id)
    if not selection or selection.student_id != student_id:
        return jsonify({'success': False, 'message': '选课记录不存在'})

    selection.update_status('cancelled')
    return jsonify({'success': True, 'message': '已取消选课'})


# ============================================================
# 成绩查询（需求11: 查询成绩）
# ============================================================

@student_bp.route('/my-grades', methods=['GET'])
def list_my_grades():
    student_id, err, resp = student_required()
    if err:
        return resp

    grades = Grade.find_by_student(student_id)
    items = [dict(r) for r in grades]
    return jsonify({'success': True, 'data': items})

# ============================================================
# 课件下载（需求11: 下载课件）
# ============================================================

@student_bp.route('/courses/<int:course_id>/download-material', methods=['GET'])
def download_course_material(course_id):
    student_id, err, resp = student_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or not course.course_material_path:
        return jsonify({'success': False, 'message': '课件不存在'})

    from flask import current_app
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], f'course_{course_id}', os.path.basename(course.course_material_path))
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': '课件文件不存在'})

    return send_from_directory(directory, filename, as_attachment=True)

# ============================================================
# 消息功能（需求12: 给任课教师发送信息和回复任课教师的留言）
# ============================================================

@student_bp.route('/messages/send', methods=['POST'])
def send_message():
    student_id, err, resp = student_required()
    if err:
        return resp

    data = request.get_json()
    receiver_id = data.get('receiver_id')
    course_id = data.get('course_id')
    content = data.get('content', '').strip()

    if not receiver_id or not content:
        return jsonify({'success': False, 'message': '接收人和消息内容不能为空'})

    msg = Message()
    msg.sender_id = student_id
    msg.receiver_id = receiver_id
    msg.course_id = course_id
    msg.content = content
    msg.save()

    return jsonify({'success': True, 'message': '发送成功', 'data': msg.to_dict()})

@student_bp.route('/messages/received', methods=['GET'])
def list_received_messages():
    student_id, err, resp = student_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    items, total = Message.find_received(student_id, page=page, page_size=page_size)
    return jsonify({
        'success': True,
        'data': {'items': items, 'total': total, 'page': page, 'page_size': page_size}
    })


@student_bp.route('/messages/sent', methods=['GET'])
def list_sent_messages():
    student_id, err, resp = student_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    items, total = Message.find_sent(student_id, page=page, page_size=page_size)
    return jsonify({
        'success': True,
        'data': {'items': items, 'total': total, 'page': page, 'page_size': page_size}
    })


@student_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
def mark_read(message_id):
    student_id, err, resp = student_required()
    if err:
        return resp

    msg = Message.find_by_id(message_id)
    if not msg or msg.receiver_id != student_id:
        return jsonify({'success': False, 'message': '消息不存在'})

    msg.mark_read()
    return jsonify({'success': True, 'message': '已标记为已读'})

@student_bp.route('/messages/<int:message_id>/reply', methods=['POST'])
def reply_message(message_id):
    student_id, err, resp = student_required()
    if err:
        return resp

    original = Message.find_by_id(message_id)
    if not original or original.receiver_id != student_id:
        return jsonify({'success': False, 'message': '原消息不存在'})

    data = request.get_json()
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'success': False, 'message': '回复内容不能为空'})

    msg = Message()
    msg.sender_id = student_id
    msg.receiver_id = original.sender_id
    msg.course_id = original.course_id
    msg.content = content
    msg.reply_to = message_id
    msg.save()

    return jsonify({'success': True, 'message': '回复成功', 'data': msg.to_dict()})
