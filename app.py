from flask import Flask, jsonify
from flask_cors import CORS

# We move our database logic into its own file (database.py) to keep app.py clean!
from database import db 
from routes.auth_routes import auth_bp  # Import our authentication APIs
from routes.quiz_routes import quiz_bp  # Import our NEW quiz APIs

# Initialize the Flask App
app = Flask(__name__)
# Enable CORS
CORS(app)

# Register our Blueprints (This attaches all routes to our main app!)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(quiz_bp, url_prefix='/api/quiz')  # Now all quiz routes start with /api/quiz

# A basic Test API Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Welcome to the Full-Stack Quiz Platform API! MongoDB is hooked up."
    }), 200

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
