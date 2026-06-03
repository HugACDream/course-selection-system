"""
成绩模型
"""


class Grade:
    """成绩类，对应 grades 表"""

    def __init__(self, row=None):
        self.id = None
        self.student_id = None
        self.course_id = None
        self.score = None        # 分数
        self.grade_point = None  # 绩点
        self.recorded_by = None  # 录入教师id
        self.recorded_at = None
        if row:
            self._from_row(row)

    def _from_row(self, row):
        self.id = row['id']
        self.student_id = row['student_id']
        self.course_id = row['course_id']
        self.score = row['score']
        self.grade_point = row['grade_point']
        self.recorded_by = row['recorded_by']
        self.recorded_at = row['recorded_at']

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'score': self.score,
            'grade_point': self.grade_point,
            'recorded_by': self.recorded_by,
            'recorded_at': str(self.recorded_at) if self.recorded_at else None,
        }

    # ---- CRUD 方法 ----

    @staticmethod
    def find_by_id(grade_id):
        """根据ID查找成绩"""
        # TODO: SELECT * FROM grades WHERE id = ?
        pass

    @staticmethod
    def find_by_student(student_id):
        """查询某学生的所有成绩"""
        # TODO: SELECT g.*, c.name as course_name FROM grades g
        #       JOIN courses c ON g.course_id = c.id WHERE g.student_id = ?
        pass

    @staticmethod
    def find_by_course(course_id):
        """查询某课程的所有学生成绩"""
        # TODO: SELECT g.*, u.name as student_name FROM grades g
        #       JOIN users u ON g.student_id = u.id WHERE g.course_id = ?
        pass

    def save(self):
        """新增或更新成绩（如果已有记录则更新）"""
        # TODO: INSERT OR REPLACE INTO grades (student_id, course_id, score, grade_point, recorded_by) VALUES (?, ?, ?, ?, ?)
        pass

    def update(self):
        """更新成绩"""
        # TODO: UPDATE grades SET score=?, grade_point=? WHERE id=?
        pass

    def delete(self):
        """删除成绩记录"""
        # TODO: DELETE FROM grades WHERE id = ?
        pass

    # ---- 统计分析 ----

    @staticmethod
    def get_statistics(course_id):
        """
        获取课程成绩统计信息
        返回: {
            'total': 总人数,
            'avg_score': 平均分,
            'max_score': 最高分,
            'min_score': 最低分,
            'pass_count': 及格人数 (>=60),
            'pass_rate': 及格率,
            'score_distribution': { '0-59': n, '60-69': n, '70-79': n, '80-89': n, '90-100': n }
        }
        """
        # TODO: 从 grades 表查询该课程所有成绩，计算各统计指标
        pass
