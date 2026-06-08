"""
用户模型 - 包含系统管理员、学院管理员、教师、学生
"""
from database import get_db

class User:
    """用户基类，对应 users 表"""

    def __init__(self, row=None):
        self.id = None
        self.username = ''
        self.password = ''
        self.role = ''         # admin / college_admin / teacher / student
        self.name = ''
        self.college_id = None
        self.email = ''
        self.phone = ''
        if row:
            self._from_row(row)

    def _from_row(self, row):
        self.id = row['id']
        self.username = row['username']
        self.password = row['password']
        self.role = row['role']
        self.name = row['name']
        self.college_id = row['college_id']
        self.email = row['email']
        self.phone = row['phone']
        self.college_name = row['college_name'] if 'college_name' in row.keys() else None

    def to_dict(self):
        d = {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'name': self.name,
            'college_id': self.college_id,
            'college_name': self.college_name,
            'email': self.email,
            'phone': self.phone,
        }
        return {k: v for k, v in d.items() if v is not None}


    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        row = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if row:
            return User(row)
        return None

    @staticmethod
    def find_by_username(username):
        db = get_db()
        row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if row:
            return User(row)
        return None


    @staticmethod
    def find_all(role=None, college_id=None, keyword='', page=1, page_size=20):
        db = get_db()
        conditions = []
        params = []

        if role:
            conditions.append('u.role = ?')
            params.append(role)
        if college_id is not None:
            conditions.append('u.college_id = ?')
            params.append(college_id)
        if keyword:
            conditions.append('(u.username LIKE ? OR u.name LIKE ?)')
            params.extend([f'%{keyword}%', f'%{keyword}%'])

        where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''

        base_from = 'FROM users u LEFT JOIN colleges c ON u.college_id = c.id'

        count_row = db.execute(
            f'SELECT COUNT(*) as cnt {base_from}{where_clause}', params
        ).fetchone()
        total = count_row['cnt']

        offset = (page - 1) * page_size
        rows = db.execute(
            f'SELECT u.*, c.name as college_name {base_from}{where_clause} ORDER BY u.id LIMIT ? OFFSET ?',
            params + [page_size, offset]
        ).fetchall()

        users = [User(r) for r in rows]
        return users, total


    def save(self):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO users (username, password, role, name, college_id, email, phone) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (self.username, self.password, self.role, self.name,
            self.college_id, self.email, self.phone)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self


    def update(self):
        db = get_db()
        db.execute(
            'UPDATE users SET name=?, college_id=?, email=?, phone=? WHERE id=?',
            (self.name, self.college_id, self.email, self.phone, self.id)
        )
        db.commit()


    def delete(self):
        db = get_db()
        db.execute('DELETE FROM users WHERE id = ?', (self.id,))
        db.commit()


    def check_password(self, password):
        return self.password == password


    
