"""
系统管理员路由
需求1: 对学生、教师、选课和课程成绩进行增、删、改和查
需求2: 对学生选择课程进行查询统计，生成柱状图并导出
"""

from flask import Blueprint, request, jsonify, session
from database import get_db
from models.user import User
from models.course import Course
from models.grade import Grade
from models.selection import CourseSelection

admin_bp = Blueprint('admin', __name__)


def admin_required():
    """装饰器：校验当前用户是否为系统管理员"""
    # TODO: 从 session 获取当前用户，检查 role == 'admin'
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return jsonify({'success': False, 'message': '无权限，需要系统管理员登录'}), 403
    return None


# ============================================================
# 学生管理 CRUD（需求1: 对学生增删改查）
# ============================================================

@admin_bp.route('/students', methods=['GET'])
def list_students():
    # 校验管理员权限
    err = admin_required()
    if err:
        return err

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    college_id = request.args.get('college_id', None, type=int)
    keyword = request.args.get('keyword', '').strip()

    users, total = User.find_all(role='student', college_id=college_id,
                                  page=page, page_size=page_size)

    # TODO: 后续在 find_all 中加入 keyword 搜索支持
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



@admin_bp.route('/students', methods=['POST'])
def create_student():
    err = admin_required()
    if err:
        return err

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()

    if not username or not password or not name:
        return jsonify({'success': False, 'message': '学号、密码和姓名不能为空'})

    # 检查用户名是否已存在
    existing = User.find_by_username(username)
    if existing:
        return jsonify({'success': False, 'message': '该用户名已存在'})

    if data.get('college_id'):
        from database import get_db
        db = get_db()
        row = db.execute('SELECT id FROM colleges WHERE id = ?', (data.get('college_id'),)).fetchone()
        if not row:
            return jsonify({'success': False, 'message': '指定的学院不存在'})

    try:
        user = User()
        user.username = username
        user.password = password
        user.role = 'student'
        user.name = name
        user.college_id = data.get('college_id')
        user.email = data.get('email', '').strip()
        user.phone = data.get('phone', '').strip()
        user.save()
        return jsonify({'success': True, 'message': '新增学生成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})



@admin_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    err = admin_required()
    if err:
        return err

    user = User.find_by_id(student_id)
    if not user or user.role != 'student':
        return jsonify({'success': False, 'message': '学生不存在'})

    return jsonify({'success': True, 'user': user.to_dict()})



@admin_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    err = admin_required()
    if err:
        return err

    user = User.find_by_id(student_id)
    if not user or user.role != 'student':
        return jsonify({'success': False, 'message': '学生不存在'})

    data = request.get_json()
    if data.get('college_id'):
        from database import get_db
        db = get_db()
        row = db.execute('SELECT id FROM colleges WHERE id = ?', (data.get('college_id'),)).fetchone()
        if not row:
            return jsonify({'success': False, 'message': '指定的学院不存在'})

    try:
        user.name = data.get('name', user.name)
        user.college_id = data.get('college_id', user.college_id)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.update()
        return jsonify({'success': True, 'message': '修改成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})



@admin_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    err = admin_required()
    if err:
        return err

    user = User.find_by_id(student_id)
    if not user or user.role != 'student':
        return jsonify({'success': False, 'message': '学生不存在'})

    user.delete()
    return jsonify({'success': True, 'message': '删除成功'})



# ============================================================
# 教师管理 CRUD（需求1: 对教师增删改查）
# ============================================================

@admin_bp.route('/teachers', methods=['GET'])
def list_teachers():
    err = admin_required()
    if err:
        return err

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    college_id = request.args.get('college_id', None, type=int)

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


@admin_bp.route('/teachers', methods=['POST'])
def create_teacher():
    err = admin_required()
    if err:
        return err

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()

    if not username or not password or not name:
        return jsonify({'success': False, 'message': '工号、密码和姓名不能为空'})

    existing = User.find_by_username(username)
    if existing:
        return jsonify({'success': False, 'message': '该用户名已存在'})

    if data.get('college_id'):
        from database import get_db
        db = get_db()
        row = db.execute('SELECT id FROM colleges WHERE id = ?', (data.get('college_id'),)).fetchone()
        if not row:
            return jsonify({'success': False, 'message': '指定的学院不存在'})

    try:
        user = User()
        user.username = username
        user.password = password
        user.role = 'teacher'
        user.name = name
        user.college_id = data.get('college_id')
        user.email = data.get('email', '').strip()
        user.phone = data.get('phone', '').strip()
        user.save()
        return jsonify({'success': True, 'message': '新增教师成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@admin_bp.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    err = admin_required()
    if err:
        return err

    user = User.find_by_id(teacher_id)
    if not user or user.role != 'teacher':
        return jsonify({'success': False, 'message': '教师不存在'})

    return jsonify({'success': True, 'user': user.to_dict()})


@admin_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    err = admin_required()
    if err:
        return err

    user = User.find_by_id(teacher_id)
    if not user or user.role != 'teacher':
        return jsonify({'success': False, 'message': '教师不存在'})

    data = request.get_json()
    if data.get('college_id'):
        from database import get_db
        db = get_db()
        row = db.execute('SELECT id FROM colleges WHERE id = ?', (data.get('college_id'),)).fetchone()
        if not row:
            return jsonify({'success': False, 'message': '指定的学院不存在'})

    try:
        user.name = data.get('name', user.name)
        user.college_id = data.get('college_id', user.college_id)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.update()
        return jsonify({'success': True, 'message': '修改成功', 'user': user.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@admin_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    err = admin_required()
    if err:
        return err

    user = User.find_by_id(teacher_id)
    if not user or user.role != 'teacher':
        return jsonify({'success': False, 'message': '教师不存在'})

    user.delete()
    return jsonify({'success': True, 'message': '删除成功'})



# ============================================================
# 课程管理 CRUD（需求1: 对选课增删改查）
# ============================================================

@admin_bp.route('/courses', methods=['GET'])
def list_courses():
    err = admin_required()
    if err:
        return err

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    college_id = request.args.get('college_id', None, type=int)
    teacher_id = request.args.get('teacher_id', None, type=int)

    courses, total = Course.find_all(college_id=college_id, teacher_id=teacher_id,
                                      page=page, page_size=page_size)
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

@admin_bp.route('/courses', methods=['POST'])
def create_course():
    err = admin_required()
    if err:
        return err

    data = request.get_json()
    name = data.get('name', '').strip()

    if not name:
        return jsonify({'success': False, 'message': '课程名称不能为空'})
    if not data.get('teacher_id'):
        return jsonify({'success': False, 'message': '请选择授课教师'})
    if not data.get('college_id'):
        return jsonify({'success': False, 'message': '请选择所属学院'})

    # 校验外键是否存在
    teacher = User.find_by_id(data.get('teacher_id'))
    if not teacher or teacher.role != 'teacher':
        return jsonify({'success': False, 'message': '指定的教师不存在'})
    from database import get_db
    db = get_db()
    college = db.execute('SELECT id FROM colleges WHERE id = ?', (data.get('college_id'),)).fetchone()
    if not college:
        return jsonify({'success': False, 'message': '指定的学院不存在'})

    try:
        course = Course()
        course.name = name
        course.description = data.get('description', '').strip()
        course.credits = data.get('credits', 0.0)
        course.teacher_id = data.get('teacher_id')
        course.college_id = data.get('college_id')
        course.max_students = data.get('max_students', 30)
        course.prerequisites = data.get('prerequisites', [])
        course.syllabus = data.get('syllabus', '').strip()
        course.save()
        return jsonify({'success': True, 'message': '新增课程成功', 'course': course.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})

@admin_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    err = admin_required()
    if err:
        return err

    course = Course.find_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': '课程不存在'})

    return jsonify({'success': True, 'course': course.to_dict()})

@admin_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    err = admin_required()
    if err:
        return err

    course = Course.find_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': '课程不存在'})

    data = request.get_json()
    if data.get('college_id'):
        from database import get_db
        db = get_db()
        row = db.execute('SELECT id FROM colleges WHERE id = ?', (data.get('college_id'),)).fetchone()
        if not row:
            return jsonify({'success': False, 'message': '指定的学院不存在'})
    if data.get('teacher_id'):
        teacher = User.find_by_id(data.get('teacher_id'))
        if not teacher or teacher.role != 'teacher':
            return jsonify({'success': False, 'message': '指定的教师不存在'})

    try:
        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        course.credits = data.get('credits', course.credits)
        course.teacher_id = data.get('teacher_id', course.teacher_id)
        course.college_id = data.get('college_id', course.college_id)
        course.max_students = data.get('max_students', course.max_students)
        course.prerequisites = data.get('prerequisites', course.prerequisites)
        course.syllabus = data.get('syllabus', course.syllabus)
        course.update()
        return jsonify({'success': True, 'message': '修改成功', 'course': course.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})

@admin_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    err = admin_required()
    if err:
        return err

    course = Course.find_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': '课程不存在'})

    course.delete()
    return jsonify({'success': True, 'message': '删除成功'})

# ============================================================
# 成绩管理 CRUD（需求1: 对课程成绩增删改查）
# ============================================================

@admin_bp.route('/grades', methods=['GET'])
def list_grades():
    err = admin_required()
    if err:
        return err

    db = get_db()
    course_id = request.args.get('course_id', None, type=int)
    student_id = request.args.get('student_id', None, type=int)
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    conditions = []
    params = []
    if course_id:
        conditions.append('g.course_id = ?')
        params.append(course_id)
    if student_id:
        conditions.append('g.student_id = ?')
        params.append(student_id)

    where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''

    count_row = db.execute(
        f'SELECT COUNT(*) as cnt FROM grades g{where_clause}', params
    ).fetchone()
    total = count_row['cnt']

    offset = (page - 1) * page_size
    rows = db.execute(
        f'SELECT g.*, u.name as student_name, c.name as course_name '
        f'FROM grades g JOIN users u ON g.student_id = u.id '
        f'JOIN courses c ON g.course_id = c.id '
        f'{where_clause} LIMIT ? OFFSET ?',
        params + [page_size, offset]
    ).fetchall()

    items = [dict(r) for r in rows]
    return jsonify({
        'success': True,
        'data': {'items': items, 'total': total, 'page': page, 'page_size': page_size}
    })


@admin_bp.route('/grades', methods=['POST'])
def create_grade():
    err = admin_required()
    if err:
        return err

    data = request.get_json()
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    score = data.get('score')

    if not student_id or not course_id:
        return jsonify({'success': False, 'message': '学生ID和课程ID不能为空'})

    # 校验学生是否存在
    student = User.find_by_id(student_id)
    if not student or student.role != 'student':
        return jsonify({'success': False, 'message': '指定的学生不存在'})
    # 校验课程是否存在
    course = Course.find_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': '指定的课程不存在'})

    try:
        grade = Grade()
        grade.student_id = student_id
        grade.course_id = course_id
        grade.score = score
        grade.grade_point = None  # TODO: 后续根据 score 自动计算绩点
        grade.recorded_by = session['user']['id']
        grade.save()
        return jsonify({'success': True, 'message': '成绩录入成功', 'grade': grade.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@admin_bp.route('/grades/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    err = admin_required()
    if err:
        return err

    grade = Grade.find_by_id(grade_id)
    if not grade:
        return jsonify({'success': False, 'message': '成绩记录不存在'})

    data = request.get_json()
    try:
        grade.score = data.get('score', grade.score)
        grade.save()
        return jsonify({'success': True, 'message': '修改成功', 'grade': grade.to_dict()})
    except Exception as e:
        get_db().rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})


@admin_bp.route('/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    err = admin_required()
    if err:
        return err

    grade = Grade.find_by_id(grade_id)
    if not grade:
        return jsonify({'success': False, 'message': '成绩记录不存在'})

    grade.delete()
    return jsonify({'success': True, 'message': '删除成功'})


# ============================================================
# 学院管理
# ============================================================

@admin_bp.route('/colleges', methods=['GET'])
def list_colleges():
    err = admin_required()
    if err:
        return err

    db = get_db()
    rows = db.execute('SELECT * FROM colleges ORDER BY id').fetchall()
    colleges = [{'id': r['id'], 'name': r['name'], 'description': r['description']} for r in rows]

    return jsonify({'success': True, 'data': colleges})


@admin_bp.route('/colleges', methods=['POST'])
def create_college():
    err = admin_required()
    if err:
        return err

    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()

    if not name:
        return jsonify({'success': False, 'message': '学院名称不能为空'})

    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO colleges (name, description) VALUES (?, ?)',
            (name, description)
        )
        db.commit()
        return jsonify({
            'success': True,
            'message': '新增学院成功',
            'college': {'id': cursor.lastrowid, 'name': name, 'description': description}
        })
    except:
        return jsonify({'success': False, 'message': '学院名称已存在'})


# ============================================================
# 选课统计（需求2: 对学生选择课程进行查询统计，生成柱状图并导出）
# ============================================================

@admin_bp.route('/statistics/course-selection', methods=['GET'])
def course_selection_statistics():
    err = admin_required()
    if err:
        return err

    stats = Course.get_selection_statistics()
    return jsonify({'success': True, 'data': stats})


@admin_bp.route('/statistics/course-selection/export', methods=['GET'])
def export_course_selection_statistics():
    """导出选课统计数据为Excel或CSV"""
    # TODO: 获取选课统计数据，生成CSV/Excel文件并返回下载
    return jsonify({'success': False, 'message': 'TODO: 导出统计待实现'})
