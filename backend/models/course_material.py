"""
课件模型 — 多文件支持
"""
import os
from database import get_db


class CourseMaterial:
    def __init__(self, row=None):
        self.id = None
        self.course_id = None
        self.filename = ''
        self.file_path = ''
        self.file_size = 0
        self.uploaded_by = None
        self.uploaded_at = None
        if row:
            self._from_row(row)

    def _from_row(self, row):
        self.id = row['id']
        self.course_id = row['course_id']
        self.filename = row['filename']
        self.file_path = row['file_path']
        self.file_size = row['file_size']
        self.uploaded_by = row['uploaded_by']
        self.uploaded_at = row['uploaded_at']

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'uploaded_at': str(self.uploaded_at) if self.uploaded_at else None,
        }

    @staticmethod
    def find_by_course(course_id):
        db = get_db()
        rows = db.execute(
            'SELECT * FROM course_materials WHERE course_id = ? ORDER BY uploaded_at DESC',
            (course_id,)
        ).fetchall()
        return [CourseMaterial(r) for r in rows]

    @staticmethod
    def find_by_id(material_id):
        db = get_db()
        row = db.execute('SELECT * FROM course_materials WHERE id = ?', (material_id,)).fetchone()
        if row:
            return CourseMaterial(row)
        return None

    def save(self):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO course_materials (course_id, filename, file_path, file_size, uploaded_by) '
            'VALUES (?, ?, ?, ?, ?)',
            (self.course_id, self.filename, self.file_path, self.file_size, self.uploaded_by)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self

    def delete(self):
        db = get_db()
        db.execute('DELETE FROM course_materials WHERE id = ?', (self.id,))
        db.commit()
        # 删除物理文件
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
