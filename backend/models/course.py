"""
课程模型
"""

import json
from database import get_db


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
        db = get_db()
        row = db.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
        if row:
            return Course(row)
        return None


    @staticmethod
    def find_all(college_id=None, teacher_id=None, keyword='', page=1, page_size=20):
        db = get_db()
        conditions = []
        params = []

        if college_id is not None:
            conditions.append('college_id = ?')
            params.append(college_id)
        if teacher_id is not None:
            conditions.append('teacher_id = ?')
            params.append(teacher_id)
        if keyword:
            conditions.append('name LIKE ?')
            params.append(f'%{keyword}%')

        where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''

        count_row = db.execute(
            f'SELECT COUNT(*) as cnt FROM courses{where_clause}', params
        ).fetchone()
        total = count_row['cnt']

        offset = (page - 1) * page_size
        rows = db.execute(
            f'SELECT * FROM courses{where_clause} ORDER BY id LIMIT ? OFFSET ?',
            params + [page_size, offset]
        ).fetchall()

        courses = [Course(r) for r in rows]
        return courses, total


    @staticmethod
    def find_by_college(college_id):
        db = get_db()
        rows = db.execute(
            'SELECT * FROM courses WHERE college_id = ?', (college_id,)
        ).fetchall()
        return [Course(r) for r in rows]


    @staticmethod
    def find_by_teacher(teacher_id):
        db = get_db()
        rows = db.execute(
            'SELECT * FROM courses WHERE teacher_id = ?', (teacher_id,)
        ).fetchall()
        return [Course(r) for r in rows]


    def save(self):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO courses (name, description, credits, teacher_id, college_id, '
            'max_students, prerequisites, syllabus, course_material_path) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (self.name, self.description, self.credits, self.teacher_id,
            self.college_id, self.max_students,
            json.dumps(self.prerequisites),
            self.syllabus, self.course_material_path)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self


    def update(self):
        db = get_db()
        db.execute(
            'UPDATE courses SET name=?, description=?, credits=?, teacher_id=?, '
            'college_id=?, max_students=?, prerequisites=?, syllabus=?, '
            'course_material_path=? WHERE id=?',
            (self.name, self.description, self.credits, self.teacher_id,
            self.college_id, self.max_students,
            json.dumps(self.prerequisites),
            self.syllabus, self.course_material_path, self.id)
        )
        db.commit()


    def delete(self):
        db = get_db()
        db.execute('DELETE FROM courses WHERE id = ?', (self.id,))
        db.commit()


    @staticmethod
    def get_selection_count(course_id):
        db = get_db()
        row = db.execute(
            "SELECT COUNT(*) as cnt FROM course_selections "
            "WHERE course_id = ? AND status != 'cancelled'",
            (course_id,)
        ).fetchone()
        return row['cnt']


    @staticmethod
    def get_selection_statistics():
        db = get_db()
        rows = db.execute(
            "SELECT c.id, c.name, COUNT(cs.id) as count "
            "FROM courses c LEFT JOIN course_selections cs "
            "ON c.id = cs.course_id AND cs.status != 'cancelled' "
            "GROUP BY c.id"
        ).fetchall()
        return [
            {'course_id': r['id'], 'course_name': r['name'], 'count': r['count']}
            for r in rows
        ]

