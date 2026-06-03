"""
选课记录模型
"""
import random
from database import get_db

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
        db = get_db()
        row = db.execute('SELECT * FROM course_selections WHERE id = ?', (selection_id,)).fetchone()
        if row:
            return CourseSelection(row)
        return None


    @staticmethod
    def find_by_student(student_id):
        db = get_db()
        rows = db.execute(
            'SELECT cs.*, c.name as course_name, c.credits '
            'FROM course_selections cs '
            'JOIN courses c ON cs.course_id = c.id '
            'WHERE cs.student_id = ?',
            (student_id,)
        ).fetchall()
        return [dict(r) for r in rows]


    @staticmethod
    def find_by_course(course_id, status=None):
        db = get_db()
        if status:
            rows = db.execute(
                'SELECT cs.*, u.name as student_name FROM course_selections cs '
                'JOIN users u ON cs.student_id = u.id '
                'WHERE cs.course_id = ? AND cs.status = ?',
                (course_id, status)
            ).fetchall()
        else:
            rows = db.execute(
                'SELECT cs.*, u.name as student_name FROM course_selections cs '
                'JOIN users u ON cs.student_id = u.id '
                'WHERE cs.course_id = ?',
                (course_id,)
            ).fetchall()
        return [dict(r) for r in rows]


    @staticmethod
    def find_confirmed_by_course(course_id):
        db = get_db()
        rows = db.execute(
            'SELECT cs.*, u.name, u.username, u.email, u.phone '
            'FROM course_selections cs '
            'JOIN users u ON cs.student_id = u.id '
            'WHERE cs.course_id = ? AND cs.status = ?',
            (course_id, 'confirmed')
        ).fetchall()
        return [dict(r) for r in rows]


    @staticmethod
    def check_exists(student_id, course_id):
        db = get_db()
        row = db.execute(
            'SELECT * FROM course_selections WHERE student_id = ? AND course_id = ? AND status != ?',
            (student_id, course_id, 'cancelled')
        ).fetchone()
        return row is not None


    def save(self):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO course_selections (student_id, course_id, status) VALUES (?, ?, ?)',
            (self.student_id, self.course_id, self.status)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self


    def update_status(self, status):
        db = get_db()
        db.execute(
            'UPDATE course_selections SET status = ? WHERE id = ?',
            (status, self.id)
        )
        db.commit()
        self.status = status


    def delete(self):
        db = get_db()
        db.execute('DELETE FROM course_selections WHERE id = ?', (self.id,))
        db.commit()

    # ---- 抽签相关 ----

    @staticmethod
    def lottery_for_course(course_id, max_students):
        db = get_db()
        rows = db.execute(
            'SELECT * FROM course_selections WHERE course_id = ? AND status = ?',
            (course_id, 'pending')
        ).fetchall()

        selections = [CourseSelection(r) for r in rows]

        if len(selections) <= max_students:
            # 全部中签
            for s in selections:
                s.update_status('confirmed')
            return [s.to_dict() for s in selections]

        # 随机抽取
        confirmed = random.sample(selections, max_students)
        confirmed_ids = {s.id for s in confirmed}

        for s in selections:
            if s.id in confirmed_ids:
                s.update_status('confirmed')
            else:
                s.update_status('cancelled')

        return [s.to_dict() for s in confirmed]
