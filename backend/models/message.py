"""
消息模型
"""
from database import get_db


class Message:
    """消息类，对应 messages 表"""

    def __init__(self, row=None):
        self.id = None
        self.sender_id = None
        self.receiver_id = None
        self.course_id = None
        self.content = ''
        self.reply_to = None        # 回复的消息id
        self.is_read = 0
        self.created_at = None
        if row:
            self._from_row(row)

    def _from_row(self, row):
        self.id = row['id']
        self.sender_id = row['sender_id']
        self.receiver_id = row['receiver_id']
        self.course_id = row['course_id']
        self.content = row['content']
        self.reply_to = row['reply_to']
        self.is_read = row['is_read']
        self.created_at = row['created_at']

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'course_id': self.course_id,
            'content': self.content,
            'reply_to': self.reply_to,
            'is_read': self.is_read,
            'created_at': str(self.created_at) if self.created_at else None,
        }

    # ---- CRUD 方法 ----

    @staticmethod
    def find_by_id(message_id):
        db = get_db()
        row = db.execute('SELECT * FROM messages WHERE id = ?', (message_id,)).fetchone()
        if row:
            return Message(row)
        return None


    @staticmethod
    def find_received(user_id, page=1, page_size=20):
        db = get_db()
        count_row = db.execute(
            'SELECT COUNT(*) as cnt FROM messages WHERE receiver_id = ?',
            (user_id,)
        ).fetchone()
        total = count_row['cnt']

        offset = (page - 1) * page_size
        rows = db.execute(
            'SELECT m.*, u.name as sender_name FROM messages m '
            'JOIN users u ON m.sender_id = u.id '
            'WHERE m.receiver_id = ? ORDER BY m.created_at DESC LIMIT ? OFFSET ?',
            (user_id, page_size, offset)
        ).fetchall()

        items = [dict(r) for r in rows]
        return items, total


    @staticmethod
    def find_sent(user_id, page=1, page_size=20):
        db = get_db()
        count_row = db.execute(
            'SELECT COUNT(*) as cnt FROM messages WHERE sender_id = ?',
            (user_id,)
        ).fetchone()
        total = count_row['cnt']

        offset = (page - 1) * page_size
        rows = db.execute(
            'SELECT m.*, u.name as receiver_name FROM messages m '
            'JOIN users u ON m.receiver_id = u.id '
            'WHERE m.sender_id = ? ORDER BY m.created_at DESC LIMIT ? OFFSET ?',
            (user_id, page_size, offset)
        ).fetchall()

        items = [dict(r) for r in rows]
        return items, total


    @staticmethod
    def find_conversation(user1_id, user2_id, course_id=None):
        """查询两个用户之间的对话历史（按课程）"""
        # TODO: SELECT * FROM messages
        #       WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
        #       AND course_id=? ORDER BY created_at ASC
        pass

    @staticmethod
    def get_unread_count(user_id):
        db = get_db()
        row = db.execute(
            'SELECT COUNT(*) as cnt FROM messages WHERE receiver_id = ? AND is_read = 0',
            (user_id,)
        ).fetchone()
        return row['cnt']


    def save(self):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO messages (sender_id, receiver_id, course_id, content, reply_to) '
            'VALUES (?, ?, ?, ?, ?)',
            (self.sender_id, self.receiver_id, self.course_id, self.content, self.reply_to)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self


    def mark_read(self):
        db = get_db()
        db.execute('UPDATE messages SET is_read = 1 WHERE id = ?', (self.id,))
        db.commit()
        self.is_read = 1

