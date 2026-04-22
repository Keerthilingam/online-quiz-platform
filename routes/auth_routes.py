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
    admin_secret = data.get('admin_secret', '')

    # SECURITY CHECK: Make sure sneaky students can't just send "role": "admin"
    if role == 'admin':
        if admin_secret != 'TEACHER123':
            return jsonify({"error": "Nice try! You need the secret Teacher Code to be an admin."}), 403

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

# ----------------------------------------------------
# 3. API: Manage Users (Admin Feature)
# ----------------------------------------------------
@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    # 1. Grab token to prove they are admin
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "VIP Wristband missing!"}), 403
        
    try:
        # Separate the word 'Bearer' from the actual token
        if "Bearer " in token:
            token_string = token.split(" ")[1] 
        else:
            token_string = token

        # Crack the token open
        decoded_data = jwt.decode(token_string, os.getenv('SECRET_KEY', 'super_secret_key_for_jwt'), algorithms=["HS256"])
        if decoded_data.get('role') != 'admin':
            return jsonify({"error": "Unauthorized! Only admins can view the user list."}), 403
    except Exception as e:
        return jsonify({"error": "Invalid or expired token!"}), 403

    # 2. Get all users, but HIDE their passwords! {"password": 0} means "hide this"
    all_users = list(db.users.find({}, {"_id": 0, "password": 0}))
    
    return jsonify({"users": all_users}), 200
