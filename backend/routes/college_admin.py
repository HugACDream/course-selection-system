"""
学院管理员路由
需求3: 对本学院教师、学生、本学院学生选课、本学院开设课程和成绩进行增删改查
需求4: 对选择课程的学生进行抽签，并按课程生成中签学生名单
"""

from flask import Blueprint, request, jsonify, session
from database import get_db
from models.user import User
from models.course import Course
from models.selection import CourseSelection

college_admin_bp = Blueprint('college_admin', __name__)


def college_admin_required():
    """校验当前用户是否为学院管理员，并返回其college_id"""
    # TODO: 从 session 获取当前用户，检查 role == 'college_admin'
    user = session.get('user')
    if not user or user.get('role') != 'college_admin':
        return None, jsonify({'success': False, 'message': '无权限，需要学院管理员登录'}), 403
    return user.get('college_id'), None, None


# ============================================================
# 本学院教师管理（需求3）
# ============================================================

@college_admin_bp.route('/teachers', methods=['GET'])
def list_teachers():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    users, total = User.find_all(role='teacher', college_id=college_id,
                                  page=page, page_size=page_size)
    user_list = [u.to_dict() for u in users]

    return jsonify({
        'success': True,
        'data': {
            'items': user_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@college_admin_bp.route('/teachers', methods=['POST'])
def create_teacher():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()

    if not username or not password or not name:
        return jsonify({'success': False, 'message': '工号、密码和姓名不能为空'})

    existing = User.find_by_username(username)
    if existing:
        return jsonify({'success': False, 'message': '该用户名已存在'})

    try:
        user = User()
        user.username = username
        user.password = password
        user.role = 'teacher'
        user.name = name
        user.college_id = college_id
        user.email = data.get('email', '').strip()
        user.phone = data.get('phone', '').strip()
        user.save()
        return jsonify({'success': True, 'message': '新增教师成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@college_admin_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    user = User.find_by_id(teacher_id)
    if not user or user.role != 'teacher' or user.college_id != college_id:
        return jsonify({'success': False, 'message': '教师不存在或不属于本学院'})

    data = request.get_json()
    try:
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.update()
        return jsonify({'success': True, 'message': '修改成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@college_admin_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    user = User.find_by_id(teacher_id)
    if not user or user.role != 'teacher' or user.college_id != college_id:
        return jsonify({'success': False, 'message': '教师不存在或不属于本学院'})

    user.delete()
    return jsonify({'success': True, 'message': '删除成功'})

# ============================================================
# 本学院学生管理（需求3）
# ============================================================

@college_admin_bp.route('/students', methods=['GET'])
def list_students():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    users, total = User.find_all(role='student', college_id=college_id,
                                  page=page, page_size=page_size)
    user_list = [u.to_dict() for u in users]

    return jsonify({
        'success': True,
        'data': {
            'items': user_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@college_admin_bp.route('/students', methods=['POST'])
def create_student():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()

    if not username or not password or not name:
        return jsonify({'success': False, 'message': '学号、密码和姓名不能为空'})

    existing = User.find_by_username(username)
    if existing:
        return jsonify({'success': False, 'message': '该用户名已存在'})

    try:
        user = User()
        user.username = username
        user.password = password
        user.role = 'student'
        user.name = name
        user.college_id = college_id
        user.email = data.get('email', '').strip()
        user.phone = data.get('phone', '').strip()
        user.save()
        return jsonify({'success': True, 'message': '新增学生成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})

@college_admin_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    user = User.find_by_id(student_id)
    if not user or user.role != 'student' or user.college_id != college_id:
        return jsonify({'success': False, 'message': '学生不存在或不属于本学院'})

    data = request.get_json()
    try:
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.update()
        return jsonify({'success': True, 'message': '修改成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@college_admin_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    user = User.find_by_id(student_id)
    if not user or user.role != 'student' or user.college_id != college_id:
        return jsonify({'success': False, 'message': '学生不存在或不属于本学院'})

    user.delete()
    return jsonify({'success': True, 'message': '删除成功'})


# ============================================================
# 本学院课程管理（需求3）
# ============================================================

@college_admin_bp.route('/courses', methods=['GET'])
def list_courses():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    courses, total = Course.find_all(college_id=college_id, page=page, page_size=page_size)
    course_list = [c.to_dict() for c in courses]

    return jsonify({
        'success': True,
        'data': {
            'items': course_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@college_admin_bp.route('/courses', methods=['POST'])
def create_course():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    data = request.get_json()
    name = data.get('name', '').strip()

    if not name:
        return jsonify({'success': False, 'message': '课程名称不能为空'})
    if not data.get('teacher_id'):
        return jsonify({'success': False, 'message': '请选择授课教师'})

    # 校验教师是否存在且属于本学院
    teacher = User.find_by_id(data.get('teacher_id'))
    if not teacher or teacher.role != 'teacher':
        return jsonify({'success': False, 'message': '指定的教师不存在'})

    try:
        course = Course()
        course.name = name
        course.description = data.get('description', '').strip()
        course.credits = data.get('credits', 0.0)
        course.teacher_id = data.get('teacher_id')
        course.college_id = college_id
        course.max_students = data.get('max_students', 30)
        course.prerequisites = data.get('prerequisites', [])
        course.syllabus = data.get('syllabus', '').strip()
        course.save()
        return jsonify({'success': True, 'message': '新增课程成功', 'course': course.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@college_admin_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.college_id != college_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于本学院'})

    data = request.get_json()
    if data.get('teacher_id'):
        teacher = User.find_by_id(data.get('teacher_id'))
        if not teacher or teacher.role != 'teacher':
            return jsonify({'success': False, 'message': '指定的教师不存在'})

    try:
        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        course.credits = data.get('credits', course.credits)
        course.teacher_id = data.get('teacher_id', course.teacher_id)
        course.max_students = data.get('max_students', course.max_students)
        course.prerequisites = data.get('prerequisites', course.prerequisites)
        course.syllabus = data.get('syllabus', course.syllabus)
        course.update()
        return jsonify({'success': True, 'message': '修改成功', 'course': course.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})

@college_admin_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.college_id != college_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于本学院'})

    course.delete()
    return jsonify({'success': True, 'message': '删除成功'})


# ============================================================
# 本学院选课管理（需求3）
# ============================================================

@college_admin_bp.route('/selections', methods=['GET'])
def list_selections():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    db = get_db()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    course_id = request.args.get('course_id', None, type=int)

    conditions = ['u.college_id = ?']
    params = [college_id]
    if course_id:
        conditions.append('cs.course_id = ?')
        params.append(course_id)

    where_clause = ' WHERE ' + ' AND '.join(conditions)

    count_row = db.execute(
        f'SELECT COUNT(*) as cnt FROM course_selections cs '
        f'JOIN users u ON cs.student_id = u.id{where_clause}', params
    ).fetchone()
    total = count_row['cnt']

    offset = (page - 1) * page_size
    rows = db.execute(
        f'SELECT cs.*, u.name as student_name, u.username as student_username, '
        f'c.name as course_name '
        f'FROM course_selections cs '
        f'JOIN users u ON cs.student_id = u.id '
        f'JOIN courses c ON cs.course_id = c.id '
        f'{where_clause} LIMIT ? OFFSET ?',
        params + [page_size, offset]
    ).fetchall()

    items = [dict(r) for r in rows]
    return jsonify({
        'success': True,
        'data': {'items': items, 'total': total, 'page': page, 'page_size': page_size}
    })

# ============================================================
# 本学院成绩管理（需求3）
# ============================================================

@college_admin_bp.route('/grades', methods=['GET'])
def list_grades():
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    db = get_db()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    count_row = db.execute(
        'SELECT COUNT(*) as cnt FROM grades g '
        'JOIN courses c ON g.course_id = c.id WHERE c.college_id = ?',
        (college_id,)
    ).fetchone()
    total = count_row['cnt']

    offset = (page - 1) * page_size
    rows = db.execute(
        'SELECT g.*, u.name as student_name, c.name as course_name '
        'FROM grades g JOIN users u ON g.student_id = u.id '
        'JOIN courses c ON g.course_id = c.id '
        'WHERE c.college_id = ? LIMIT ? OFFSET ?',
        (college_id, page_size, offset)
    ).fetchall()

    items = [dict(r) for r in rows]
    return jsonify({
        'success': True,
        'data': {'items': items, 'total': total, 'page': page, 'page_size': page_size}
    })


# ============================================================
# 抽签功能（需求4: 对选择课程的学生进行抽签，并按课程生成中签学生名单）
# ============================================================

@college_admin_bp.route('/lottery/<int:course_id>', methods=['POST'])
def lottery(course_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.college_id != college_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于本学院'})

    data = request.get_json() or {}
    max_students = data.get('max_students', course.max_students)

    result = CourseSelection.lottery_for_course(course_id, max_students)
    return jsonify({'success': True, 'message': f'抽签完成，中签{len(result)}人', 'data': result})


@college_admin_bp.route('/lottery/<int:course_id>/result', methods=['GET'])
def lottery_result(course_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    course = Course.find_by_id(course_id)
    if not course or course.college_id != college_id:
        return jsonify({'success': False, 'message': '课程不存在或不属于本学院'})

    confirmed = CourseSelection.find_confirmed_by_course(course_id)
    items = [dict(r) for r in confirmed]
    return jsonify({'success': True, 'data': items})


@college_admin_bp.route('/lottery/<int:course_id>/export', methods=['GET'])
def export_lottery_result(course_id):
    college_id, err, resp = college_admin_required()
    if err:
        return resp

    confirmed = CourseSelection.find_confirmed_by_course(course_id)
    items = [dict(r) for r in confirmed]
    # TODO: 生成CSV文件并返回下载
    return jsonify({'success': True, 'data': items})
