import sqlite3
from datetime import datetime
import os

class CaseManagement:
    def __init__(self):
        self.db_path = 'cases.db'
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建案例表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            methods TEXT,
            results TEXT,
            conclusions TEXT,
            author TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tags TEXT,
            likes INTEGER DEFAULT 0
        )
        ''')
        
        # 创建评论表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            user_id INTEGER,
            content TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # 创建图片表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS case_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            image_path TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_case(self, title, description, methods, results, conclusions, author, tags):
        """添加新案例"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO cases (title, description, methods, results, conclusions, author, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, methods, results, conclusions, author, ','.join(tags)))
            
            case_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True, case_id
        except Exception as e:
            return False, str(e)
    
    def add_case_image(self, case_id, image_path):
        """添加案例图片"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO case_images (case_id, image_path)
            VALUES (?, ?)
            ''', (case_id, image_path))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False, str(e)
    
    def add_comment(self, case_id, user_id, content):
        """添加评论"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO comments (case_id, user_id, content)
            VALUES (?, ?, ?)
            ''', (case_id, user_id, content))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False, str(e)
    
    def like_case(self, case_id):
        """点赞案例"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE cases SET likes = likes + 1
            WHERE id = ?
            ''', (case_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False, str(e)
    
    def get_cases(self, sort_by="date", tags=None, limit=10):
        """获取案例列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM cases"
            params = []
            
            if tags:
                tag_conditions = []
                for tag in tags:
                    tag_conditions.append("tags LIKE ?")
                    params.append(f"%{tag}%")
                if tag_conditions:
                    query += " WHERE " + " OR ".join(tag_conditions)
            
            if sort_by == "最新发布":
                query += " ORDER BY date DESC"
            elif sort_by == "最多点赞":
                query += " ORDER BY likes DESC"
            
            query += " LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            cases = cursor.fetchall()
            
            # 获取每个案例的图片
            result = []
            for case in cases:
                cursor.execute('SELECT image_path FROM case_images WHERE case_id = ?', (case[0],))
                images = cursor.fetchall()
                
                cursor.execute('SELECT COUNT(*) FROM comments WHERE case_id = ?', (case[0],))
                comment_count = cursor.fetchone()[0]
                
                case_dict = {
                    'id': case[0],
                    'title': case[1],
                    'description': case[2],
                    'methods': case[3],
                    'results': case[4],
                    'conclusions': case[5],
                    'author': case[6],
                    'date': case[7],
                    'tags': case[8].split(',') if case[8] else [],
                    'likes': case[9],
                    'images': [img[0] for img in images],
                    'comment_count': comment_count
                }
                result.append(case_dict)
            
            conn.close()
            return result
        except Exception as e:
            return []
    
    def get_case_comments(self, case_id):
        """获取案例评论"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT c.*, u.username 
            FROM comments c
            LEFT JOIN users u ON c.user_id = u.id
            WHERE c.case_id = ?
            ORDER BY c.date DESC
            ''', (case_id,))
            
            comments = cursor.fetchall()
            conn.close()
            
            return [{
                'id': c[0],
                'content': c[3],
                'date': c[4],
                'username': c[5] or "匿名用户"
            } for c in comments]
        except Exception as e:
            return [] 