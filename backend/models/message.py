"""
消息模型
"""


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
        """根据ID查找消息"""
        # TODO: SELECT * FROM messages WHERE id = ?
        pass

    @staticmethod
    def find_received(user_id, page=1, page_size=20):
        """查询某用户收到的消息列表"""
        # TODO: SELECT m.*, u.name as sender_name FROM messages m
        #       JOIN users u ON m.sender_id = u.id WHERE m.receiver_id = ? ORDER BY m.created_at DESC
        pass

    @staticmethod
    def find_sent(user_id, page=1, page_size=20):
        """查询某用户发送的消息列表"""
        # TODO: SELECT m.*, u.name as receiver_name FROM messages m
        #       JOIN users u ON m.receiver_id = u.id WHERE m.sender_id = ? ORDER BY m.created_at DESC
        pass

    @staticmethod
    def find_conversation(user1_id, user2_id, course_id=None):
        """查询两个用户之间的对话历史（按课程）"""
        # TODO: SELECT * FROM messages
        #       WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
        #       AND course_id=? ORDER BY created_at ASC
        pass

    @staticmethod
    def get_unread_count(user_id):
        """获取未读消息数"""
        # TODO: SELECT COUNT(*) FROM messages WHERE receiver_id = ? AND is_read = 0
        pass

    def save(self):
        """发送新消息"""
        # TODO: INSERT INTO messages (sender_id, receiver_id, course_id, content, reply_to) VALUES (?, ?, ?, ?, ?)
        pass

    def mark_read(self):
        """标记为已读"""
        # TODO: UPDATE messages SET is_read = 1 WHERE id = ?
        pass
