from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load our .env file so we can read MONGO_URI
load_dotenv()

# Get the URL (fallback to localhost if .env is somehow missing)
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/quiz_db")

# Initialize the MongoClient
client = MongoClient(mongo_uri)

# Select and expose our "quiz_db" database 
# We will import this 'db' variable in other files!
db = client.get_database()
