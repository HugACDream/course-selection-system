"""
系统管理员服务
"""


class AdminService:
    """系统管理员相关业务逻辑"""

    # ---- 用户管理 ----

    @staticmethod
    def create_user(username, password, role, name, college_id=None, email='', phone=''):
        """创建用户（学生/教师/学院管理员）"""
        # TODO: 1. 检查 username 是否已存在
        # TODO: 2. 创建 User 对象并设置属性
        # TODO: 3. 密码处理（生产环境需哈希）
        # TODO: 4. 调用 user.save() 保存到数据库
        pass

    @staticmethod
    def get_users(role=None, college_id=None, keyword='', page=1, page_size=20):
        """分页查询用户列表"""
        # TODO: 调用 User.find_all(role, college_id, page, page_size)
        pass

    @staticmethod
    def delete_user(user_id):
        """删除用户（需校验不能删除自己）"""
        # TODO: 1. 查找用户是否存在
        # TODO: 2. 调用 user.delete()
        pass

    # ---- 成绩管理 ----

    @staticmethod
    def create_or_update_grade(student_id, course_id, score, recorded_by):
        """创建或更新成绩"""
        # TODO: 1. 查找是否已有成绩记录
        # TODO: 2. 计算 grade_point（绩点换算）
        # TODO: 3. 创建或更新记录
        pass

    # ---- 统计 ----

    @staticmethod
    def get_course_selection_stats():
        """
        获取选课统计数据
        返回: [ { course_id, course_name, student_count }, ... ]
        """
        # TODO: 调用 Course.get_selection_statistics()
        pass

    @staticmethod
    def export_to_csv(data, filename):
        """将数据导出为CSV文件"""
        # TODO: 1. 使用 csv 模块将数据写入临时文件
        # TODO: 2. 返回文件路径供下载
        pass
