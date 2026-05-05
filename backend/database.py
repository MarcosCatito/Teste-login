import sqlite3
import hashlib
from datetime import datetime
from security import security, secure_database_query

class Database:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_username 
            ON users(username)
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @secure_database_query
    def create_user(self, username, password, email=None):
        # Validar e sanitizar inputs
        valid_username, username = security.validate_username(username)
        if not valid_username:
            return False, username
        
        valid_email, email = security.validate_email(email)
        if not valid_email:
            return False, email
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, "Username already exists"
            
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, created_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (username, password_hash, email))
            
            user_id = cursor.lastrowid
            conn.commit()
            return True, {"id": user_id, "username": username}
            
        except sqlite3.Error as e:
            conn.rollback()
            return False, "Database error"
        finally:
            conn.close()
    
    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND is_active = 1",
                (username,)
            )
            user = cursor.fetchone()
            return dict(user) if user else None
        except sqlite3.Error:
            return None
        finally:
            conn.close()
    
    def verify_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                SELECT id, username, email FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            if user:
                cursor.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                    (user['id'],)
                )
                conn.commit()
                return dict(user)
            return None
        except sqlite3.Error:
            return None
        finally:
            conn.close()
    
    def update_user(self, user_id, username=None, email=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if username:
                updates.append("username = ?")
                params.append(username)
            if email:
                updates.append("email = ?")
                params.append(email)
            
            if not updates:
                return False, "No fields to update"
            
            params.append(user_id)
            
            sql = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, params)
            conn.commit()
            return True, "User updated successfully"
            
        except sqlite3.IntegrityError:
            conn.rollback()
            return False, "Username already exists"
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Database error: {e}"
        finally:
            conn.close()
    
    def delete_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE users SET is_active = 0 WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, username, email, created_at, last_login 
                FROM users 
                WHERE is_active = 1 
                ORDER BY created_at DESC
            ''')
            users = cursor.fetchall()
            return [dict(user) for user in users]
        except sqlite3.Error:
            return []
        finally:
            conn.close()
    
    def get_user_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            stats = {}
            cursor.execute(
                "SELECT COUNT(*) as total FROM users WHERE is_active = 1"
            )
            stats['total_users'] = cursor.fetchone()['total']
            
            cursor.execute('''
                SELECT COUNT(*) as today 
                FROM users 
                WHERE DATE(created_at) = DATE('now') AND is_active = 1
            ''')
            stats['users_today'] = cursor.fetchone()['today']
            
            return stats
        except sqlite3.Error:
            return {}
        finally:
            conn.close()

db = Database()
