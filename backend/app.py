from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import hashlib
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'

# In-memory user storage (for demo purposes)
users = {}

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
            
            if username in users:
                return render_template('index.html', show_success=False, error='Username already exists')
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            users[username] = hashed_password
            
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
        
        if username in users:
            return jsonify({'error': 'Username already exists'}), 400
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        users[username] = hashed_password
        
        token = generate_token(username)
        
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': username
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        # Check if it's a form submission (from integrated frontend)
        if request.content_type and 'application/json' not in request.content_type:
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return render_template('index.html', show_success=False, error='Username and password required')
            
            if username not in users:
                return render_template('index.html', show_success=False, error='Invalid credentials')
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            if users[username] != hashed_password:
                return render_template('index.html', show_success=False, error='Invalid credentials')
            
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
        
        if username not in users:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if users[username] != hashed_password:
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
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    username = session.get('username', 'User')
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'This is a protected route'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
