from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import db  # Import our database connection!
import datetime
import jwt
import os

# Create a Blueprint named 'auth'
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # 1. Grab the JSON data the user sent
    data = request.get_json()

    # 2. Extract email and password safely
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user') # Default everyone to 'user' role unless specified

    # 3. Simple Validation
    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    # 4. Check if the user already exists in the "users" collection
    existing_user = db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "Email already exists in our system."}), 400

    # 5. Hash the password for security (NEVER store plain-text passwords!)
    hashed_password = generate_password_hash(password)

    # 6. Create the new user dictionary (This is our "table design" essentially!)
    new_user = {
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.datetime.utcnow()
    }

    # 7. Insert into the MongoDB "users" collection
    db.users.insert_one(new_user)

    # 8. Return success response
    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    # 1. Grab data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # 2. Find the user in the database
    user = db.users.find_one({"email": email})

    # 3. If user doesn't exist OR the password doesn't match the scrambled hash
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # 4. If correct, we generate a VIP Pass (JWT Token) for the user
    secret_key = os.getenv('SECRET_KEY', 'super_secret_key_for_jwt')
    token = jwt.encode(
        {
            "user_id": str(user['_id']), 
            "role": user.get('role', 'user'), 
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Ticket expires in 24 hrs
        },
        secret_key,
        algorithm="HS256"
    )

    return jsonify({"message": "Login successful!", "token": token}), 200
