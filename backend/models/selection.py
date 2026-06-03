"""
选课记录模型
"""


class CourseSelection:
    """选课记录类，对应 course_selections 表"""

    def __init__(self, row=None):
        self.id = None
        self.student_id = None
        self.course_id = None
        self.status = 'pending'   # pending=待抽签, confirmed=中签, cancelled=已取消
        self.selected_at = None
        if row:
            self._from_row(row)

    def _from_row(self, row):
        self.id = row['id']
        self.student_id = row['student_id']
        self.course_id = row['course_id']
        self.status = row['status']
        self.selected_at = row['selected_at']

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'status': self.status,
            'selected_at': str(self.selected_at) if self.selected_at else None,
        }

    # ---- CRUD 方法 ----

    @staticmethod
    def find_by_id(selection_id):
        """根据ID查找选课记录"""
        # TODO: SELECT * FROM course_selections WHERE id = ?
        pass

    @staticmethod
    def find_by_student(student_id):
        """查询某学生的所有选课记录"""
        # TODO: SELECT cs.*, c.name as course_name, c.credits FROM course_selections cs
        #       JOIN courses c ON cs.course_id = c.id WHERE cs.student_id = ?
        pass

    @staticmethod
    def find_by_course(course_id, status=None):
        """查询某课程的所有选课学生"""
        # TODO: SELECT cs.*, u.name as student_name FROM course_selections cs
        #       JOIN users u ON cs.student_id = u.id WHERE cs.course_id = ? AND status = ?
        pass

    @staticmethod
    def find_confirmed_by_course(course_id):
        """查询某课程中签学生名单"""
        # TODO: SELECT cs.*, u.name, u.email, u.phone FROM course_selections cs
        #       JOIN users u ON cs.student_id = u.id WHERE cs.course_id = ? AND cs.status = 'confirmed'
        pass

    @staticmethod
    def check_exists(student_id, course_id):
        """检查学生是否已经选择了某课程"""
        # TODO: SELECT * FROM course_selections WHERE student_id = ? AND course_id = ?
        pass

    def save(self):
        """新增选课记录"""
        # TODO: INSERT INTO course_selections (student_id, course_id, status) VALUES (?, ?, ?)
        pass

    def update_status(self, status):
        """更新选课状态（用于抽签确认）"""
        # TODO: UPDATE course_selections SET status = ? WHERE id = ?
        pass

    def delete(self):
        """删除选课记录（取消选课）"""
        # TODO: DELETE FROM course_selections WHERE id = ?
        pass

    # ---- 抽签相关 ----

    @staticmethod
    def lottery_for_course(course_id, max_students):
        """
        对某课程进行抽签，随机选出中签学生
        返回中签学生名单
        """
        # TODO: 1. 查询该课程所有 pending 状态的选课记录
        # TODO: 2. 如果选课人数 <= max_students，全部中签
        # TODO: 3. 否则随机抽取 max_students 人，其余标记为 cancelled
        # TODO: 4. 返回中签学生列表
        pass
