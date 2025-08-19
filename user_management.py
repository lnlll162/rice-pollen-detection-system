import sqlite3
import hashlib
import re
from datetime import datetime
import os

class UserManagement:
    def __init__(self):
        self.db_path = 'users.db'
        self.init_database()
        self.create_admin_if_not_exists()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT UNIQUE,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_admin_if_not_exists(self):
        """创建默认管理员账号"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查是否存在管理员账号
            cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                # 创建默认管理员账号
                admin_password = self.hash_password("admin123")
                cursor.execute('''
                INSERT INTO users (username, password, role, email)
                VALUES (?, ?, ?, ?)
                ''', ("admin", admin_password, "admin", "admin@example.com"))
                conn.commit()
            
            conn.close()
        except Exception as e:
            print(f"创建管理员账号时出错：{e}")
    
    def hash_password(self, password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email):
        """验证邮箱格式"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """验证手机号格式"""
        pattern = r'^1[3-9]\d{9}$'
        return re.match(pattern, phone) is not None
    
    def register_user(self, username, password, email=None, phone=None, role='user'):
        """用户注册"""
        try:
            if not username or not password:
                return False, "用户名和密码为必填项"
                
            # 验证邮箱格式
            if email and not self.validate_email(email):
                return False, "邮箱格式不正确"
            
            # 验证手机号格式
            if phone and not self.validate_phone(phone):
                return False, "手机号格式不正确"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查用户名是否已存在
            cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False, "用户名已存在"
            
            # 检查邮箱是否已存在（如果提供了邮箱）
            if email:
                cursor.execute('SELECT COUNT(*) FROM users WHERE email = ? AND email IS NOT NULL', (email,))
                if cursor.fetchone()[0] > 0:
                    conn.close()
                    return False, "邮箱已被注册"
            
            # 检查手机号是否已存在（如果提供了手机号）
            if phone:
                cursor.execute('SELECT COUNT(*) FROM users WHERE phone = ? AND phone IS NOT NULL', (phone,))
                if cursor.fetchone()[0] > 0:
                    conn.close()
                    return False, "手机号已被注册"
            
            # 将空字符串转换为 None
            email = email if email and email.strip() else None
            phone = phone if phone and phone.strip() else None
            
            hashed_password = self.hash_password(password)
            cursor.execute('''
            INSERT INTO users (username, password, email, phone, role, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, email, phone, role, 'active'))
            
            conn.commit()
            conn.close()
            return True, "注册成功"
            
        except Exception as e:
            return False, f"注册失败：{str(e)}"
    
    def login(self, identifier, password):
        """用户登录"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 支持使用用户名、邮箱或手机号登录
            cursor.execute('''
            SELECT id, username, role, password, status FROM users 
            WHERE username = ? OR email = ? OR phone = ?
            ''', (identifier, identifier, identifier))
            
            user = cursor.fetchone()
            if not user:
                return False, "用户不存在"
            
            if user[4] != 'active':
                return False, "账号已被禁用"
            
            if user and user[3] == self.hash_password(password):
                # 更新最后登录时间
                cursor.execute('''
                UPDATE users SET last_login = ? WHERE id = ?
                ''', (datetime.now(), user[0]))
                conn.commit()
                conn.close()
                return True, {"id": user[0], "username": user[1], "role": user[2]}
            
            conn.close()
            return False, "用户名或密码错误"
        except Exception as e:
            return False, f"登录失败：{str(e)}"
    
    def get_user_role(self, user_id):
        """获取用户角色"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
        role = cursor.fetchone()
        conn.close()
        return role[0] if role else None
    
    def get_all_users(self):
        """获取所有用户信息（管理员使用）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, username, email, phone, role, status, created_at, last_login 
            FROM users
            ''')
            users = cursor.fetchall()
            conn.close()
            
            return [{
                "id": user[0],
                "username": user[1],
                "email": user[2] or "",
                "phone": user[3] or "",
                "role": user[4],
                "status": user[5],
                "created_at": user[6],
                "last_login": user[7] or ""
            } for user in users]
        except Exception as e:
            print(f"获取用户列表失败：{e}")
            return []
    
    def disable_user(self, username):
        """禁用用户（管理员使用）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET status = "disabled" WHERE username = ?', (username,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"禁用用户失败：{e}")
            return False
    
    def enable_user(self, username):
        """启用用户（管理员使用）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET status = "active" WHERE username = ?', (username,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"启用用户失败：{e}")
            return False
    
    def delete_user(self, username):
        """删除用户（管理员使用）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE username = ? AND role != "admin"', (username,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除用户失败：{e}")
            return False 