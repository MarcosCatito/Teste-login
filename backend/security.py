import re
import hashlib
import time
from functools import wraps
from flask import request, jsonify, g
import sqlite3

class SecurityManager:
    def __init__(self):
        self.failed_attempts = {}
        self.rate_limits = {}
    
    def sanitize_input(self, input_string):
        """Sanitiza entrada para prevenir SQL Injection e XSS"""
        if not input_string:
            return ""
        
        # Remover caracteres perigosos para SQL Injection
        dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_', '0x']
        sanitized = input_string
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Remover tags HTML (XSS protection)
        sanitized = re.sub(r'<[^>]*>', '', sanitized)
        
        # Limitar tamanho
        sanitized = sanitized[:100]
        
        return sanitized.strip()
    
    def validate_username(self, username):
        """Valida username com regras estritas"""
        if not username:
            return False, "Username is required"
        
        # Sanitizar entrada
        username = self.sanitize_input(username)
        
        # Verificar comprimento
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 50:
            return False, "Username must be less than 50 characters"
        
        # Verificar formato (apenas letras, números e underscore)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers and underscores"
        
        # Verificar se não são palavras reservadas
        reserved_words = ['admin', 'root', 'system', 'null', 'undefined', 'drop', 'delete', 'insert', 'update']
        if username.lower() in reserved_words:
            return False, "Username is reserved"
        
        return True, username
    
    def validate_email(self, email):
        """Valida email com regras estritas"""
        if not email:
            return True, ""  # Email é opcional
        
        email = self.sanitize_input(email).lower()
        
        # Verificar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        # Limitar tamanho
        if len(email) > 100:
            return False, "Email is too long"
        
        return True, email
    
    def check_rate_limit(self, identifier, limit=5, window=300):
        """Rate limiting para prevenir brute force"""
        now = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Remover tentativas antigas
        self.rate_limits[identifier] = [
            timestamp for timestamp in self.rate_limits[identifier]
            if now - timestamp < window
        ]
        
        # Verificar limite
        if len(self.rate_limits[identifier]) >= limit:
            return False, f"Rate limit exceeded. Try again in {window} seconds."
        
        # Adicionar tentativa atual
        self.rate_limits[identifier].append(now)
        return True, "OK"
    
    def check_brute_force(self, ip_address, username=None):
        """Verifica tentativas de brute force"""
        key = f"{ip_address}:{username}" if username else ip_address
        
        if key not in self.failed_attempts:
            self.failed_attempts[key] = []
        
        now = time.time()
        
        # Remover tentativas antigas (15 minutos)
        self.failed_attempts[key] = [
            timestamp for timestamp in self.failed_attempts[key]
            if now - timestamp < 900
        ]
        
        # Se houver mais de 5 tentativas falhadas
        if len(self.failed_attempts[key]) >= 5:
            return False, "Too many failed attempts. Try again later."
        
        return True, "OK"
    
    def record_failed_attempt(self, ip_address, username=None):
        """Regista tentativa falhada"""
        key = f"{ip_address}:{username}" if username else ip_address
        if key not in self.failed_attempts:
            self.failed_attempts[key] = []
        self.failed_attempts[key].append(time.time())
    
    def clear_failed_attempts(self, ip_address, username=None):
        """Limpa tentativas falhadas após login bem-sucedido"""
        key = f"{ip_address}:{username}" if username else ip_address
        if key in self.failed_attempts:
            del self.failed_attempts[key]

# Instância global do gestor de segurança
security = SecurityManager()

def secure_input(func):
    """Decorator para validar e sanitizar entradas"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Obter IP do cliente
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        # Rate limiting
        rate_ok, rate_msg = security.check_rate_limit(client_ip)
        if not rate_ok:
            return jsonify({'error': rate_msg}), 429
        
        # Para endpoints POST, validar dados
        if request.method == 'POST':
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            if 'username' in data:
                valid, result = security.validate_username(data['username'])
                if not valid:
                    return jsonify({'error': result}), 400
                data['username'] = result
            
            if 'email' in data:
                valid, result = security.validate_email(data['email'])
                if not valid:
                    return jsonify({'error': result}), 400
                if result:  # Se email foi fornecido
                    data['email'] = result
        
        return func(*args, **kwargs)
    return decorated_function

def secure_database_query(func):
    """Decorator para segurança em operações de base de dados"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            # Log do erro (sem expor detalhes sensíveis)
            print(f"Database error: {str(e)}")
            return jsonify({'error': 'Database operation failed'}), 500
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function
