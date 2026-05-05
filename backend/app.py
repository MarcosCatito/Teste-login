from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import hashlib
import jwt
import datetime
from functools import wraps
from database import db
from security import security, secure_input, secure_database_query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# CORS seguro - apenas permite origens específicas em produção
CORS(app, 
     origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
     methods=['GET', 'POST', 'PUT', 'DELETE'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = False  # True em produção com HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Base de dados SQL para utilizadores
# A variável 'users' foi substituída pela base de dados SQLite
# Ver database.py para implementação completa

def validate_password(password):
    """Validate password with enhanced security requirements"""
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    
    if not has_lower:
        return False, "Password must contain at least one lowercase letter"
    
    if not has_digit:
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

def generate_token(username):
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            jwt.decode(token.split()[1], app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
@secure_input
def register():
    try:
        # Check if it's a form submission (from integrated frontend)
        if request.content_type and 'application/json' not in request.content_type:
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return render_template('index.html', show_success=False, error='Username and password required')
            
            if len(username) < 3:
                return render_template('index.html', show_success=False, error='Username must be at least 3 characters')
            
            # Validate password with enhanced security
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                return render_template('index.html', show_success=False, error=error_msg)
            
            # Criar utilizador na base de dados
            success, result = db.create_user(username, password)
            if not success:
                return render_template('index.html', show_success=False, error=result)
            
            # Store session
            session['username'] = username
            session['logged_in'] = True
            
            return redirect(url_for('dashboard'))
        
        # Handle JSON requests (for API usage)
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        username = data['username']
        password = data['password']
        
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        # Validate password with enhanced security
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Criar utilizador na base de dados
        success, result = db.create_user(username, password)
        if not success:
            return jsonify({'error': result}), 400
        
        token = generate_token(username)
        
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': username
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
@secure_input
def login():
    try:
        # Obter IP do cliente para segurança
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        # Check if it's a form submission (from integrated frontend)
        if request.content_type and 'application/json' not in request.content_type:
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return render_template('index.html', show_success=False, error='Username and password required')
            
            # Verificar brute force
            brute_ok, brute_msg = security.check_brute_force(client_ip, username)
            if not brute_ok:
                return render_template('index.html', show_success=False, error=brute_msg)
            
            # Verificar credenciais na base de dados
            user = db.verify_user(username, password)
            if not user:
                security.record_failed_attempt(client_ip, username)
                return render_template('index.html', show_success=False, error='Invalid credentials')
            
            # Limpar tentativas falhadas após sucesso
            security.clear_failed_attempts(client_ip, username)
            
            # Store session
            session['username'] = username
            session['logged_in'] = True
            
            return redirect(url_for('dashboard'))
        
        # Handle JSON requests (for API usage)
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        username = data['username']
        password = data['password']
        
        # Verificar credenciais na base de dados
        user = db.verify_user(username, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = generate_token(username)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': username
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

        
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return render_template('dashboard.html', username=session.get('username', ''))
    return redirect(url_for('index'))

@app.route('/success')
def success_page():
    """Página de sucesso para registro/login - serve template para React SPA"""
    return render_template('spa.html')  # Template específico para SPA

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'This is a protected route'})

# Novos endpoints para demonstrar capacidades SQL
@app.route('/api/users', methods=['GET'])
@token_required
def get_all_users():
    """SQL: SELECT - Obtém todos os utilizadores"""
    try:
        users = db.get_all_users()
        return jsonify({
            'users': users,
            'total': len(users)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users'}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """SQL: SELECT - Obtém utilizador por ID"""
    try:
        user = db.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user'}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """SQL: UPDATE - Atualiza utilizador"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        
        success, result = db.update_user(user_id, username, email)
        if not success:
            return jsonify({'error': result}), 400
        
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': 'Failed to update user'}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """SQL: UPDATE - Desativa utilizador (soft delete)"""
    try:
        success = db.delete_user(user_id)
        if not success:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deactivated successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to delete user'}), 500

@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats():
    """SQL: SELECT - Obtém estatísticas do sistema"""
    try:
        stats = db.get_user_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch stats'}), 500

@app.route('/api/sessions/cleanup', methods=['POST'])
@token_required
def cleanup_sessions():
    """SQL: UPDATE - Limpa sessões expiradas"""
    try:
        cleaned = db.cleanup_expired_sessions()
        return jsonify({
            'message': f'Cleaned up {cleaned} expired sessions'
        })
    except Exception as e:
        return jsonify({'error': 'Failed to cleanup sessions'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
