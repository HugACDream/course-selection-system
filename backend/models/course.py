"""
课程模型
"""

import json


class Course:
    """课程类，对应 courses 表"""

    def __init__(self, row=None):
        self.id = None
        self.name = ''
        self.description = ''
        self.credits = 0.0
        self.teacher_id = None
        self.college_id = None
        self.max_students = 30
        self.prerequisites = []      # 先修课程id列表
        self.syllabus = ''           # 课程介绍
        self.course_material_path = ''
        if row:
            self._from_row(row)

    def _from_row(self, row):
        self.id = row['id']
        self.name = row['name']
        self.description = row['description']
        self.credits = row['credits']
        self.teacher_id = row['teacher_id']
        self.college_id = row['college_id']
        self.max_students = row['max_students']
        self.prerequisites = json.loads(row['prerequisites'] or '[]')
        self.syllabus = row['syllabus'] or ''
        self.course_material_path = row['course_material_path'] or ''

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'credits': self.credits,
            'teacher_id': self.teacher_id,
            'college_id': self.college_id,
            'max_students': self.max_students,
            'prerequisites': self.prerequisites,
            'syllabus': self.syllabus,
            'course_material_path': self.course_material_path,
        }

    # ---- CRUD 方法 ----

    @staticmethod
    def find_by_id(course_id):
        """根据ID查找课程"""
        # TODO: SELECT * FROM courses WHERE id = ?
        pass

    @staticmethod
    def find_all(college_id=None, teacher_id=None, page=1, page_size=20):
        """分页查询课程列表，可按学院和教师筛选"""
        # TODO: SELECT * FROM courses WHERE college_id=? AND teacher_id=? LIMIT ? OFFSET ?
        # TODO: 返回 (课程列表, 总数)
        pass

    @staticmethod
    def find_by_college(college_id):
        """查询某学院所有课程"""
        # TODO: SELECT * FROM courses WHERE college_id = ?
        pass

    @staticmethod
    def find_by_teacher(teacher_id):
        """查询某教师的所有课程"""
        # TODO: SELECT * FROM courses WHERE teacher_id = ?
        pass

    def save(self):
        """新增课程"""
        # TODO: INSERT INTO courses (...) VALUES (...)
        pass

    def update(self):
        """更新课程信息"""
        # TODO: UPDATE courses SET name=?, description=?, credits=?, teacher_id=?, college_id=?, max_students=?, prerequisites=?, syllabus=?, course_material_path=? WHERE id=?
        pass

    def delete(self):
        """删除课程"""
        # TODO: DELETE FROM courses WHERE id = ?
        pass

    @staticmethod
    def get_selection_count(course_id):
        """获取某门课程的选课人数"""
        # TODO: SELECT COUNT(*) FROM course_selections WHERE course_id = ? AND status != 'cancelled'
        pass

    @staticmethod
    def get_selection_statistics():
        """获取每门课程的选课人数统计（用于柱状图）"""
        # TODO: SELECT c.id, c.name, COUNT(cs.id) as count
        #       FROM courses c LEFT JOIN course_selections cs ON c.id = cs.course_id
        #       WHERE cs.status != 'cancelled'
        #       GROUP BY c.id
        pass
