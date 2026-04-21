from flask import Blueprint, request, jsonify
from database import db
import jwt
import os
from functools import wraps

# ----------------------------------------------------
# THE BOUNCER (admin_required Decorator)
# ----------------------------------------------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Look for the 'Authorization' token in the Postman headers
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({"error": "VIP Wristband (Token) is missing!"}), 403
            
        try:
            # Postman sends it as "Bearer <token>", so we separate it to get just the random letters
            if "Bearer " in token:
                token_string = token.split(" ")[1] 
            else:
                token_string = token

            # 2. Crack open the token to read the data inside
            decoded_data = jwt.decode(token_string, os.getenv('SECRET_KEY', 'super_secret_key_for_jwt'), algorithms=["HS256"])
            
            # 3. Check if the role is admin
            if decoded_data.get('role') != 'admin':
                return jsonify({"error": "Unauthorized! Only admins can add questions."}), 403
                
        except Exception as e:
            return jsonify({"error": "Invalid or expired token!"}), 403
            
        # 4. If everything is good, let them pass!
        return f(*args, **kwargs)
    return decorated

# Create a new Blueprint (Department) specifically for Quizzes
quiz_bp = Blueprint('quiz', __name__)

# ----------------------------------------------------
# 1. API: Add a New Question (Admin Feature)
# ----------------------------------------------------
@quiz_bp.route('/add-question', methods=['POST'])
@admin_required  # <--- WE ADDED THE BOUNCER HERE!
def add_question():
    data = request.get_json()
    
    # Grab the data from the request
    subject = data.get('subject')        # e.g., 'Python' or 'SQL'
    set_name = data.get('set_name')      # e.g., 'A', 'B', 'C', or 'D'
    question_text = data.get('question_text')
    options = data.get('options')
    correct_answer = data.get('correct_answer')

    # Validation: Make sure they didn't leave anything blank
    if not question_text or not options or not correct_answer or not subject or not set_name:
        return jsonify({"error": "All fields (subject, set_name, question_text, options, correct_answer) are required!"}), 400

    # Build the dictionary (JSON) to save to MongoDB
    new_question = {
        "subject": subject,
        "set_name": set_name,
        "question_text": question_text,
        "options": options,
        "correct_answer": correct_answer
    }

    # Save it to the "questions" collection in the database
    db.questions.insert_one(new_question)

    return jsonify({"message": "Question added successfully!"}), 201

# ----------------------------------------------------
# 2. API: Get Questions by Subject & Set! (User Feature)
# ----------------------------------------------------
# Example URL: http://127.0.0.1:5000/api/quiz/questions/Python/A
@quiz_bp.route('/questions/<subject>/<set_name>', methods=['GET'])
def get_questions(subject, set_name):
    # Ask MongoDB to ONLY return questions that perfectly match the Subject AND the Set!
    questions_list = list(db.questions.find({
        "subject": subject, 
        "set_name": set_name
    }, {"_id": 0}))
    
    return jsonify({"questions": questions_list}), 200

# ----------------------------------------------------
# 3. API: Submit Quiz & Get Score (User Feature)
# ----------------------------------------------------
@quiz_bp.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    
    # We expect the frontend to send the user's email and their answers
    email = data.get('email')
    answers = data.get('answers') # Example: {"What is the capital of France?": "Paris"}

    if not email or not answers:
        return jsonify({"error": "Email and answers are required!"}), 400

    score = 0
    total_questions = len(answers)

    # Loop through each answer the user gave
    for question_text, chosen_answer in answers.items():
        # Look up the actual question in the database
        real_question = db.questions.find_one({"question_text": question_text})
        
        # If the user's answer matches the real correct answer, add +1 to their score!
        if real_question and real_question['correct_answer'] == chosen_answer:
            score += 1

    # Save this final score into a new "results" collection in MongoDB
    result_data = {
        "email": email,
        "score": score,
        "total": total_questions
    }
    db.results.insert_one(result_data)

    # Tell the user how they did!
    return jsonify({
        "message": "Quiz submitted successfully!", 
        "score": score, 
        "total": total_questions
    }), 200
