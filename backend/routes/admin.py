"""
系统管理员路由
需求1: 对学生、教师、选课和课程成绩进行增、删、改和查
需求2: 对学生选择课程进行查询统计，生成柱状图并导出
"""

from flask import Blueprint, request, jsonify, session

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
    """查询学生列表（支持分页和按学院筛选）"""
    # TODO: 校验管理员权限 admin_required()
    # TODO: 获取查询参数: page, page_size, college_id, keyword
    # TODO: 调用 User.find_all(role='student', ...) 查询学生列表
    # TODO: 返回分页数据 { success, data: { items, total, page, page_size } }
    return jsonify({'success': False, 'message': 'TODO: 查询学生列表待实现'})


@admin_bp.route('/students', methods=['POST'])
def create_student():
    """新增学生"""
    # TODO: 校验管理员权限
    # TODO: 获取请求体: { username, password, name, college_id, email, phone }
    # TODO: 创建 User 对象，设置 role='student'，调用 save()
    # TODO: 返回创建结果
    return jsonify({'success': False, 'message': 'TODO: 新增学生待实现'})


@admin_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """查询单个学生详情"""
    # TODO: 校验管理员权限
    # TODO: 调用 User.find_by_id(student_id) 查询
    return jsonify({'success': False, 'message': 'TODO: 查询学生详情待实现'})


@admin_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """修改学生信息"""
    # TODO: 校验管理员权限
    # TODO: 查找学生，更新字段，调用 update()
    return jsonify({'success': False, 'message': 'TODO: 修改学生信息待实现'})


@admin_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """删除学生"""
    # TODO: 校验管理员权限
    # TODO: 查找学生，调用 delete()
    return jsonify({'success': False, 'message': 'TODO: 删除学生待实现'})


# ============================================================
# 教师管理 CRUD（需求1: 对教师增删改查）
# ============================================================

@admin_bp.route('/teachers', methods=['GET'])
def list_teachers():
    """查询教师列表"""
    # TODO: 校验管理员权限
    # TODO: 调用 User.find_all(role='teacher', ...) 查询教师列表
    return jsonify({'success': False, 'message': 'TODO: 查询教师列表待实现'})


@admin_bp.route('/teachers', methods=['POST'])
def create_teacher():
    """新增教师"""
    # TODO: 校验管理员权限
    # TODO: 创建 User 对象，role='teacher'，调用 save()
    return jsonify({'success': False, 'message': 'TODO: 新增教师待实现'})


@admin_bp.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """查询单个教师详情"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 查询教师详情待实现'})


@admin_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """修改教师信息"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 修改教师信息待实现'})


@admin_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """删除教师"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 删除教师待实现'})


# ============================================================
# 课程管理 CRUD（需求1: 对选课增删改查）
# ============================================================

@admin_bp.route('/courses', methods=['GET'])
def list_courses():
    """查询所有课程列表"""
    # TODO: 校验管理员权限
    # TODO: 调用 Course.find_all() 查询课程列表
    return jsonify({'success': False, 'message': 'TODO: 查询课程列表待实现'})


@admin_bp.route('/courses', methods=['POST'])
def create_course():
    """新增课程"""
    # TODO: 校验管理员权限
    # TODO: 获取请求体，创建 Course 对象，调用 save()
    return jsonify({'success': False, 'message': 'TODO: 新增课程待实现'})


@admin_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """查询单个课程详情"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 查询课程详情待实现'})


@admin_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """修改课程信息"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 修改课程信息待实现'})


@admin_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """删除课程"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 删除课程待实现'})


# ============================================================
# 成绩管理 CRUD（需求1: 对课程成绩增删改查）
# ============================================================

@admin_bp.route('/grades', methods=['GET'])
def list_grades():
    """查询所有成绩记录"""
    # TODO: 校验管理员权限
    # TODO: 支持按学生、课程筛选，分页返回
    return jsonify({'success': False, 'message': 'TODO: 查询成绩列表待实现'})


@admin_bp.route('/grades', methods=['POST'])
def create_grade():
    """新增/修改成绩"""
    # TODO: 校验管理员权限
    # TODO: 创建或更新成绩记录
    return jsonify({'success': False, 'message': 'TODO: 新增成绩待实现'})


@admin_bp.route('/grades/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    """修改成绩"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 修改成绩待实现'})


@admin_bp.route('/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    """删除成绩"""
    # TODO: 校验管理员权限
    return jsonify({'success': False, 'message': 'TODO: 删除成绩待实现'})


# ============================================================
# 学院管理
# ============================================================

@admin_bp.route('/colleges', methods=['GET'])
def list_colleges():
    """查询学院列表"""
    # TODO: SELECT * FROM colleges
    return jsonify({'success': False, 'message': 'TODO: 查询学院列表待实现'})


@admin_bp.route('/colleges', methods=['POST'])
def create_college():
    """新增学院"""
    # TODO: INSERT INTO colleges (name, description) VALUES (?, ?)
    return jsonify({'success': False, 'message': 'TODO: 新增学院待实现'})


# ============================================================
# 选课统计（需求2: 对学生选择课程进行查询统计，生成柱状图并导出）
# ============================================================

@admin_bp.route('/statistics/course-selection', methods=['GET'])
def course_selection_statistics():
    """
    获取每门课的选课人数统计（用于柱状图）
    返回: { success, data: [ { course_id, course_name, count }, ... ] }
    """
    # TODO: 调用 Course.get_selection_statistics() 获取统计数据
    return jsonify({'success': False, 'message': 'TODO: 选课统计待实现'})


@admin_bp.route('/statistics/course-selection/export', methods=['GET'])
def export_course_selection_statistics():
    """导出选课统计数据为Excel或CSV"""
    # TODO: 获取选课统计数据，生成CSV/Excel文件并返回下载
    return jsonify({'success': False, 'message': 'TODO: 导出统计待实现'})
