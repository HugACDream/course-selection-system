"""
用户模型 - 包含系统管理员、学院管理员、教师、学生
"""
from database import get_db

from werkzeug.security import generate_password_hash, check_password_hash

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

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'name': self.name,
            'college_id': self.college_id,
            'email': self.email,
            'phone': self.phone,
        }

    # ---- CRUD 方法（TODO标记由后续Python实现） ----

    @staticmethod
    def find_by_id(id):
        db = get_db()
        row = db.execute('SELECT * FROM users WHERE id  = ?', (id,)).fetchone()
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
    def find_all(role=None, college_id=None, page=1, page_size=20):
        """分页查询用户列表，可按角色和学院筛选"""
        # TODO: SELECT * FROM users WHERE role=? AND college_id=? LIMIT ? OFFSET ?
        # TODO: 返回 (用户列表, 总数)
        pass

    def save(self):
        """新增用户"""
        # TODO: INSERT INTO users (username, password, role, name, college_id, email, phone) VALUES (?, ?, ?, ?, ?, ?, ?)
        pass

    def update(self):
        """更新用户信息"""
        # TODO: UPDATE users SET name=?, college_id=?, email=?, phone=? WHERE id=?
        pass

    def delete(self):
        """删除用户"""
        # TODO: DELETE FROM users WHERE id = ?
        pass

    def check_password(self, password):
        return self.password == password


    
