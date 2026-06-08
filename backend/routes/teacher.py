"""
教师路由
需求5: 输入课程介绍、上传课件、发布先修课程、更新和修改课程信息
需求6: 查询中签学生名单，录入成绩，生成成绩统计表
需求7: 对学生发送消息留言
"""
from database import get_db
from models.user import User
from models.course import Course
from models.selection import CourseSelection
from models.grade import Grade
from models.message import Message
import os

from flask import Blueprint, request, jsonify, session

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
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    courses = Course.find_by_teacher(teacher_id)
    course_list = []
    for c in courses:
        d = c.to_dict()
        d['selection_count'] = Course.get_selection_count(c.id)
        course_list.append(d)

    return jsonify({'success': True, 'data': course_list})



@teacher_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于您'})

    d = course.to_dict()
    d['selection_count'] = Course.get_selection_count(course_id)
    return jsonify({'success': True, 'course': d})


@teacher_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于您'})

    data = request.get_json()
    try:
        course.description = data.get('description', course.description)
        course.credits = data.get('credits', course.credits)
        course.max_students = data.get('max_students', course.max_students)
        course.prerequisites = data.get('prerequisites', course.prerequisites)
        course.syllabus = data.get('syllabus', course.syllabus)
        course.update()
        return jsonify({'success': True, 'message': '更新成功', 'course': course.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@teacher_bp.route('/courses/<int:course_id>/upload-material', methods=['POST'])
def upload_course_material(course_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于您'})

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '请选择文件'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '请选择文件'})

    from flask import current_app
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], f'course_{course_id}')
    os.makedirs(upload_dir, exist_ok=True)

    filename = file.filename
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    course.course_material_path = f'uploads/course_{course_id}/{filename}'
    course.update()

    return jsonify({
        'success': True,
        'message': '上传成功',
        'file_path': course.course_material_path
    })


# ============================================================
# 中签学生查询（需求6: 查询选修自己课程的所有中签学生名单）
# ============================================================

@teacher_bp.route('/courses/<int:course_id>/confirmed-students', methods=['GET'])
def get_confirmed_students(course_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于您'})

    students = CourseSelection.find_confirmed_by_course(course_id)
    return jsonify({'success': True, 'data': students})


# ============================================================
# 成绩管理（需求6: 录入课程成绩生成成绩统计表）
# ============================================================

@teacher_bp.route('/courses/<int:course_id>/grades', methods=['GET'])
def list_course_grades(course_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于您'})

    grades = Grade.find_by_course(course_id)
    items = [r.to_dict() for r in grades]
    return jsonify({'success': True, 'data': items})


@teacher_bp.route('/courses/<int:course_id>/grades', methods=['POST'])
def save_grades(course_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于您'})

    data = request.get_json()
    grades_data = data.get('grades', [])

    for item in grades_data:
        score = item.get('score')
        # 计算绩点
        if score is not None:
            if score >= 90:
                gp = 4.0
            elif score >= 80:
                gp = 3.0
            elif score >= 70:
                gp = 2.0
            elif score >= 60:
                gp = 1.0
            else:
                gp = 0.0
        else:
            gp = None

        grade = Grade()
        grade.student_id = item['student_id']
        grade.course_id = course_id
        grade.score = score
        grade.grade_point = gp
        grade.recorded_by = teacher_id
        grade.save()

    return jsonify({'success': True, 'message': f'已录入{len(grades_data)}条成绩'})


@teacher_bp.route('/courses/<int:course_id>/statistics', methods=['GET'])
def get_grade_statistics(course_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于您'})

    stats = Grade.get_statistics(course_id)
    return jsonify({'success': True, 'data': stats})



# ============================================================
# 消息功能（需求7: 对选修自己课程学生发送消息留言）
# ============================================================

@teacher_bp.route('/messages/send', methods=['POST'])
def send_message():
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    data = request.get_json()
    receiver_id = data.get('receiver_id')
    course_id = data.get('course_id')
    content = data.get('content', '').strip()
    reply_to = data.get('reply_to')

    if not receiver_id or not content:
        return jsonify({'success': False, 'message': '接收人和消息内容不能为空'})

    msg = Message()
    msg.sender_id = teacher_id
    msg.receiver_id = receiver_id
    msg.course_id = course_id
    msg.content = content
    msg.reply_to = reply_to
    msg.save()

    return jsonify({'success': True, 'message': '发送成功', 'data': msg.to_dict()})


@teacher_bp.route('/messages/received', methods=['GET'])
def list_received_messages():
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    items, total = Message.find_received(teacher_id, page=page, page_size=page_size)
    return jsonify({
        'success': True,
        'data': {'items': items, 'total': total, 'page': page, 'page_size': page_size}
    })


@teacher_bp.route('/messages/sent', methods=['GET'])
def list_sent_messages():
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    items, total = Message.find_sent(teacher_id, page=page, page_size=page_size)
    return jsonify({
        'success': True,
        'data': {'items': items, 'total': total, 'page': page, 'page_size': page_size}
    })


@teacher_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
def mark_read(message_id):
    teacher_id, err, resp = teacher_required()
    if err:
        return resp

    msg = Message.find_by_id(message_id)
    if not msg or msg.receiver_id != teacher_id:
        return jsonify({'success': False, 'message': '消息不存在'})

    msg.mark_read()
    return jsonify({'success': True, 'message': '已标记为已读'})
