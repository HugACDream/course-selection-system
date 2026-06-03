"""
学生服务
"""


class StudentService:
    """学生相关业务逻辑"""

    # ---- 选课 ----

    @staticmethod
    def get_available_courses(student_id, college_id=None, keyword=''):
        """获取可选课程列表"""
        # TODO: 1. 查询所有课程 Course.find_all()
        # TODO: 2. 附带每门课的选课人数
        # TODO: 3. 标记学生是否已选修每门课
        pass

    @staticmethod
    def select_course(student_id, course_id):
        """
        学生选课（需求8 & 10）
        返回: (success, message)
        """
        # TODO: 1. 获取课程信息 Course.find_by_id(course_id)
        # TODO: 2. 【需求10】检查先修课程：
        #         a. 获取 course.prerequisites（先修课程id列表）
        #         b. 如果 prerequisites 为空列表，跳过检查
        #         c. 查询学生成绩表 Grade.find_by_student(student_id)
        #         d. 检查每个先修课程是否在成绩表中且 score >= 60
        #         e. 如果有未通过的先修课：
        #             返回 (False, '您没有学习该课程的先修课程，不能进行选课！')
        # TODO: 3. 检查是否已选过该课程 CourseSelection.check_exists(student_id, course_id)
        #        如果已存在且未取消，返回 (False, '您已选择过该课程')
        # TODO: 4. 创建选课记录，status='pending'
        # TODO: 5. 返回 (True, '选课成功，请等待抽签结果')
        pass

    @staticmethod
    def get_my_selections(student_id):
        """查询我的选课记录（需求8 & 9）"""
        # TODO: 调用 CourseSelection.find_by_student(student_id)
        # TODO: 联表查询课程名称、教师姓名、学分等
        pass

    @staticmethod
    def cancel_selection(student_id, selection_id):
        """取消选课"""
        # TODO: 1. 验证选课记录属于该学生
        # TODO: 2. 检查选课状态（已中签的可能不能取消，看业务规则）
        # TODO: 3. 更新状态为 'cancelled'
        pass

    # ---- 成绩查询 ----

    @staticmethod
    def get_my_grades(student_id):
        """查询我的所有成绩（需求11: 查询成绩）"""
        # TODO: 调用 Grade.find_by_student(student_id)
        # TODO: 联表查询课程名称、学分、教师等
        pass

    # ---- 课件下载 ----

    @staticmethod
    def can_download_material(student_id, course_id):
        """检查学生是否有权下载某课程课件"""
        # TODO: 验证学生已中签该课程（status='confirmed'）
        pass

    # ---- 消息 ----

    @staticmethod
    def send_message_to_teacher(student_id, teacher_id, course_id, content, reply_to=None):
        """给教师发送消息（需求12: 给任课教师发送信息）"""
        # TODO: 1. 创建 Message 对象
        # TODO: 2. 调用 message.save()
        pass

    @staticmethod
    def reply_message(student_id, original_message_id, content):
        """回复教师留言（需求12: 回复任课教师的留言）"""
        # TODO: 1. 找到原消息 Message.find_by_id(original_message_id)
        # TODO: 2. 获取原消息的 sender_id（教师）和 course_id
        # TODO: 3. 创建新的 Message 记录:
        #         sender_id=student_id, receiver_id=原消息发送者
        #         course_id=原消息课程, content=content, reply_to=original_message_id
        # TODO: 4. 返回新消息
        pass

    @staticmethod
    def get_my_messages(student_id, msg_type='received'):
        """获取我的消息列表"""
        # TODO: msg_type == 'received' → Message.find_received(student_id)
        # TODO: msg_type == 'sent' → Message.find_sent(student_id)
        pass
