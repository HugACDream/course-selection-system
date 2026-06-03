"""
认证服务
"""


class AuthService:
    """登录认证相关业务逻辑"""

    @staticmethod
    def login(username, password):
        """
        用户登录验证
        返回: (success, user_dict_or_error_message)
        """
        # TODO: 1. 从数据库查找用户 User.find_by_username(username)
        # TODO: 2. 如果用户不存在，返回 (False, '用户名或密码错误')
        # TODO: 3. 校验密码 user.check_password(password)
        # TODO: 4. 如果密码错误，返回 (False, '用户名或密码错误')
        # TODO: 5. 登录成功，返回 (True, user.to_dict())
        pass

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """修改密码"""
        # TODO: 1. 查找用户
        # TODO: 2. 校验旧密码
        # TODO: 3. 更新密码（生产环境需哈希处理）
        # TODO: 4. 保存到数据库
        pass
