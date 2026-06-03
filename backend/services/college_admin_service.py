"""
学院管理员服务
"""

import random


class CollegeAdminService:
    """学院管理员相关业务逻辑"""

    @staticmethod
    def get_my_college_users(college_id, role, page=1, page_size=20):
        """查询本学院的用户（教师/学生）"""
        # TODO: 调用 User.find_all(role=role, college_id=college_id, page=page, page_size=page_size)
        pass

    @staticmethod
    def get_my_college_courses(college_id):
        """查询本学院开设的所有课程"""
        # TODO: 调用 Course.find_by_college(college_id)
        pass

    @staticmethod
    def get_my_college_selections(college_id):
        """查询本学院学生的选课记录"""
        # TODO: 联表查询 course_selections + users + courses，筛选 college_id
        pass

    # ---- 抽签 ----

    @staticmethod
    def lottery(course_id, max_students=None):
        """
        对课程进行抽签
        逻辑:
        1. 获取课程信息（如未指定max_students则使用课程的max_students）
        2. 获取所有 pending 状态的选课记录
        3. 如果选课人数 <= max_students，全部 confirmed
        4. 否则随机抽取 max_students 人，其余 cancelled
        5. 更新所有记录的状态
        6. 返回中签学生名单
        """
        # TODO: 1. course = Course.find_by_id(course_id)
        # TODO: 2. max_students = max_students or course.max_students
        # TODO: 3. selections = 该课程所有 pending 状态的选课记录
        # TODO: 4. 如果 len(selections) <= max_students: 全部设为 confirmed
        # TODO: 5. 否则 random.sample(selections, max_students) 设为 confirmed，其余为 cancelled
        # TODO: 6. 更新数据库
        # TODO: 7. 返回中签列表
        pass

    @staticmethod
    def get_lottery_result(course_id):
        """获取中签学生名单"""
        # TODO: 调用 CourseSelection.find_confirmed_by_course(course_id)
        pass

    @staticmethod
    def export_lottery_result_to_csv(course_id):
        """导出中签学生名单为CSV"""
        # TODO: 1. 获取中签名单
        # TODO: 2. 生成CSV文件
        # TODO: 3. 返回文件路径
        pass
