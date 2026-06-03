"""
成绩模型
"""

from database import get_db

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
        db = get_db()
        row = db.execute('SELECT * FROM grades WHERE id = ?', (grade_id,)).fetchone()
        if row:
            return Grade(row)
        return None

    @staticmethod
    def find_by_student(student_id):
        db = get_db()
        rows = db.execute(
            'SELECT g.*, c.name as course_name FROM grades g '
            'JOIN courses c ON g.course_id = c.id WHERE g.student_id = ?',
            (student_id,)
        ).fetchall()
        return [Grade(r) for r in rows]


    @staticmethod
    def find_by_course(course_id):
        db = get_db()
        rows = db.execute(
            'SELECT g.*, u.name as student_name FROM grades g '
            'JOIN users u ON g.student_id = u.id WHERE g.course_id = ?',
            (course_id,)
        ).fetchall()
        return [Grade(r) for r in rows]

    def save(self):
        db = get_db()
        cursor = db.execute(
            'INSERT OR REPLACE INTO grades (student_id, course_id, score, grade_point, recorded_by) '
            'VALUES (?, ?, ?, ?, ?)',
            (self.student_id, self.course_id, self.score, self.grade_point, self.recorded_by)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self

    def delete(self):
        db = get_db()
        db.execute('DELETE FROM grades WHERE id = ?', (self.id,))
        db.commit()

    # ---- 统计分析 ----

    @staticmethod
    def get_statistics(course_id):
        db = get_db()
        rows = db.execute(
            'SELECT score FROM grades WHERE course_id = ? AND score IS NOT NULL',
            (course_id,)
        ).fetchall()

        scores = [r['score'] for r in rows]
        total = len(scores)

        if total == 0:
            return {
                'total': 0, 'avg_score': 0, 'max_score': 0, 'min_score': 0,
                'pass_count': 0, 'pass_rate': 0,
                'score_distribution': {'0-59': 0, '60-69': 0, '70-79': 0, '80-89': 0, '90-100': 0}
            }

        avg_score = round(sum(scores) / total, 2)
        max_score = max(scores)
        min_score = min(scores)
        pass_count = sum(1 for s in scores if s >= 60)
        pass_rate = round(pass_count / total * 100, 2)

        distribution = {'0-59': 0, '60-69': 0, '70-79': 0, '80-89': 0, '90-100': 0}
        for s in scores:
            if s < 60:
                distribution['0-59'] += 1
            elif s < 70:
                distribution['60-69'] += 1
            elif s < 80:
                distribution['70-79'] += 1
            elif s < 90:
                distribution['80-89'] += 1
            else:
                distribution['90-100'] += 1

        return {
            'total': total,
            'avg_score': avg_score,
            'max_score': max_score,
            'min_score': min_score,
            'pass_count': pass_count,
            'pass_rate': pass_rate,
            'score_distribution': distribution,
        }

