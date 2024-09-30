from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from functools import wraps

# Load environment variables from .env
load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app)

# JWT secret key from .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY environment variable is missing")

# Database connection function
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        raise ConnectionError(f"Database connection error: {str(e)}")

# JWT Token Middleware
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        # Ensure token has the format 'Bearer <token>'
        if "Bearer " in token:
            token = token.split(" ")[1]

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError as e:
            return jsonify({'message': f'Token is invalid: {str(e)}'}), 403

        return f(current_user_id, *args, **kwargs)
    return decorator

# Helper function to handle database operations
def execute_db(query, params=(), fetch=False):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        connection.commit()
    except pymysql.MySQLError as e:
        raise RuntimeError(f"Database query error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# User registration (CREATE)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(password)

    try:
        execute_db("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# User login (Generate JWT)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    try:
        users = execute_db("SELECT * FROM users WHERE username = %s", (username,), fetch=True)
        user = users[0] if users else None

        if not user or not check_password_hash(user['password'], password):
            return jsonify({'message': 'Invalid credentials'}), 401

        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Get all users (READ)
@app.route('/users', methods=['GET'])
@token_required
def get_users(current_user_id):
    try:
        users = execute_db("SELECT id, username FROM users", fetch=True)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Update user (UPDATE)
@app.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user_id, id):
    data = request.get_json()
    new_username = data.get('username')
    new_password = data.get('password')

    if not new_username or not new_password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(new_password)

    try:
        execute_db("UPDATE users SET username = %s, password = %s WHERE id = %s", 
                   (new_username, hashed_password, id))
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Delete user (DELETE)
@app.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user_id, id):
    try:
        execute_db("DELETE FROM users WHERE id = %s", (id,))
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
