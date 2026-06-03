"""
教师服务
"""

import os


class TeacherService:
    """教师相关业务逻辑"""

    # ---- 课程管理 ----

    @staticmethod
    def get_my_courses(teacher_id):
        """查询我教授的课程"""
        # TODO: 调用 Course.find_by_teacher(teacher_id)
        pass

    @staticmethod
    def update_course_info(course_id, teacher_id, data):
        """
        更新课程信息（需求5: 输入课程介绍、发布先修课程、更新和修改课程信息）
        data可包含: name, description, credits, syllabus, prerequisites, max_students
        """
        # TODO: 1. 验证课程属于该教师
        # TODO: 2. 更新课程字段
        # TODO: 3. 调用 course.update()
        pass

    @staticmethod
    def upload_material(course_id, teacher_id, file):
        """
        上传课件（需求5: 上传课程的课件）
        """
        # TODO: 1. 验证课程属于该教师
        # TODO: 2. 创建目录 uploads/course_{course_id}/
        # TODO: 3. 保存上传的文件（注意文件名安全处理）
        # TODO: 4. 更新 course.course_material_path
        # TODO: 5. 返回文件访问URL
        pass

    # ---- 学生与成绩 ----

    @staticmethod
    def get_confirmed_students(course_id, teacher_id):
        """查询中签学生名单（需求6）"""
        # TODO: 1. 验证课程属于该教师
        # TODO: 2. 调用 CourseSelection.find_confirmed_by_course(course_id)
        pass

    @staticmethod
    def save_grades(course_id, teacher_id, grades_data):
        """
        录入成绩（需求6: 录入课程成绩）
        grades_data: [ { student_id, score }, ... ]
        """
        # TODO: 1. 验证课程属于该教师
        # TODO: 2. 遍历 grades_data
        # TODO: 3. 为每条记录计算 grade_point:
        #          score >= 90 → 4.0
        #          score >= 80 → 3.0
        #          score >= 70 → 2.0
        #          score >= 60 → 1.0
        #          score < 60  → 0.0
        # TODO: 4. 调用 Grade.save() 或 INSERT OR REPLACE
        pass

    @staticmethod
    def get_grade_statistics(course_id, teacher_id):
        """
        生成成绩统计表（需求6: 每个分数段的人数，及格率等）
        返回格式:
        {
            'total': 总人数,
            'avg_score': 平均分,
            'max_score': 最高分,
            'min_score': 最低分,
            'pass_count': 及格人数 (>=60),
            'pass_rate': 及格率 (0-100),
            'score_distribution': {
                '0-59': n, '60-69': n, '70-79': n, '80-89': n, '90-100': n
            }
        }
        """
        # TODO: 1. 验证课程属于该教师
        # TODO: 2. 调用 Grade.get_statistics(course_id)
        pass

    # ---- 消息 ----

    @staticmethod
    def send_message(sender_id, receiver_id, course_id, content, reply_to=None):
        """发送消息（需求7: 对选修自己课程学生发送消息留言）"""
        # TODO: 1. 创建 Message 对象
        # TODO: 2. 调用 message.save()
        pass

    @staticmethod
    def get_messages(user_id, msg_type='received'):
        """获取消息列表"""
        # TODO: msg_type == 'received' → Message.find_received(user_id)
        # TODO: msg_type == 'sent' → Message.find_sent(user_id)
        pass
