"""
学院管理员路由
需求3: 对本学院教师、学生、本学院学生选课、本学院开设课程和成绩进行增删改查
需求4: 对选择课程的学生进行抽签，并按课程生成中签学生名单
"""

from flask import Blueprint, request, jsonify, session

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
    """查询本学院教师列表"""
    # TODO: college_id, err, resp = college_admin_required() → 校验
    # TODO: 调用 User.find_all(role='teacher', college_id=college_id) 查询
    return jsonify({'success': False, 'message': 'TODO: 查询本学院教师待实现'})


@college_admin_bp.route('/teachers', methods=['POST'])
def create_teacher():
    """新增本学院教师"""
    # TODO: 校验权限，获取 college_id
    # TODO: 创建 User 对象，role='teacher', college_id=college_id，调用 save()
    return jsonify({'success': False, 'message': 'TODO: 新增本学院教师待实现'})


@college_admin_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """修改本学院教师信息"""
    # TODO: 校验权限，验证该教师属于本学院
    return jsonify({'success': False, 'message': 'TODO: 修改本学院教师待实现'})


@college_admin_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """删除本学院教师"""
    # TODO: 校验权限，验证该教师属于本学院
    return jsonify({'success': False, 'message': 'TODO: 删除本学院教师待实现'})


# ============================================================
# 本学院学生管理（需求3）
# ============================================================

@college_admin_bp.route('/students', methods=['GET'])
def list_students():
    """查询本学院学生列表"""
    # TODO: 校验权限，调用 User.find_all(role='student', college_id=college_id)
    return jsonify({'success': False, 'message': 'TODO: 查询本学院学生待实现'})


@college_admin_bp.route('/students', methods=['POST'])
def create_student():
    """新增本学院学生"""
    # TODO: 校验权限，创建学生记录
    return jsonify({'success': False, 'message': 'TODO: 新增本学院学生待实现'})


@college_admin_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """修改本学院学生信息"""
    # TODO: 校验权限，验证学生属于本学院
    return jsonify({'success': False, 'message': 'TODO: 修改本学院学生待实现'})


@college_admin_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """删除本学院学生"""
    # TODO: 校验权限
    return jsonify({'success': False, 'message': 'TODO: 删除本学院学生待实现'})


# ============================================================
# 本学院课程管理（需求3）
# ============================================================

@college_admin_bp.route('/courses', methods=['GET'])
def list_courses():
    """查询本学院开设课程列表"""
    # TODO: 校验权限，调用 Course.find_by_college(college_id)
    return jsonify({'success': False, 'message': 'TODO: 查询本学院课程待实现'})


@college_admin_bp.route('/courses', methods=['POST'])
def create_course():
    """新增本学院课程"""
    # TODO: 校验权限，创建课程记录
    return jsonify({'success': False, 'message': 'TODO: 新增本学院课程待实现'})


@college_admin_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """修改本学院课程信息"""
    # TODO: 校验权限，验证课程属于本学院
    return jsonify({'success': False, 'message': 'TODO: 修改本学院课程待实现'})


@college_admin_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """删除本学院课程"""
    # TODO: 校验权限
    return jsonify({'success': False, 'message': 'TODO: 删除本学院课程待实现'})


# ============================================================
# 本学院选课管理（需求3）
# ============================================================

@college_admin_bp.route('/selections', methods=['GET'])
def list_selections():
    """查询本学院学生选课记录"""
    # TODO: 校验权限
    # TODO: 查询本学院所有学生的选课记录
    return jsonify({'success': False, 'message': 'TODO: 查询本学院选课记录待实现'})


# ============================================================
# 本学院成绩管理（需求3）
# ============================================================

@college_admin_bp.route('/grades', methods=['GET'])
def list_grades():
    """查询本学院课程成绩"""
    # TODO: 校验权限，查询本学院课程的成绩记录
    return jsonify({'success': False, 'message': 'TODO: 查询本学院成绩待实现'})


# ============================================================
# 抽签功能（需求4: 对选择课程的学生进行抽签，并按课程生成中签学生名单）
# ============================================================

@college_admin_bp.route('/lottery/<int:course_id>', methods=['POST'])
def lottery(course_id):
    """
    对指定课程进行抽签
    请求: { max_students: 30 }（可选，默认使用课程的max_students）
    """
    # TODO: 1. 校验学院管理员权限，验证课程属于本学院
    # TODO: 2. 获取 max_students 参数
    # TODO: 3. 调用 CourseSelection.lottery_for_course(course_id, max_students)
    # TODO: 4. 返回中签学生名单
    return jsonify({'success': False, 'message': 'TODO: 抽签功能待实现'})


@college_admin_bp.route('/lottery/<int:course_id>/result', methods=['GET'])
def lottery_result(course_id):
    """查询某课程的中签学生名单"""
    # TODO: 校验权限
    # TODO: 调用 CourseSelection.find_confirmed_by_course(course_id)
    # TODO: 返回中签学生列表
    return jsonify({'success': False, 'message': 'TODO: 查询中签名单待实现'})


@college_admin_bp.route('/lottery/<int:course_id>/export', methods=['GET'])
def export_lottery_result(course_id):
    """导出某课程的中签学生名单"""
    # TODO: 获取中签名单，生成CSV/Excel文件导出
    return jsonify({'success': False, 'message': 'TODO: 导出中签名单待实现'})
