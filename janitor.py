from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load your cloud credentials
load_dotenv()
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.quiz_db

def cleanup_duplicates():
    print("Cloud Janitor is starting a deep search...")
    
    # Let's find out which database actually has the data
    db_names = client.list_database_names()
    print(f"I see these databases in your cloud: {db_names}")
    
    # We will check 'quiz_db' first, then 'test'
    target_db = None
    if 'quiz_db' in db_names: target_db = client.quiz_db
    elif 'test' in db_names: target_db = client.test
    
    if not target_db:
        print("Error: I couldn't find any questions in your cloud yet!")
        return

    all_questions = list(target_db.questions.find())
    print(f"Found {len(all_questions)} total questions in '{target_db.name}'")
    
    seen_texts = set()
    deleted_count = 0
    
    for q in all_questions:
        text = q['question_text']
        if text in seen_texts:
            target_db.questions.delete_one({'_id': q['_id']})
            deleted_count += 1
        else:
            seen_texts.add(text)
            
    print(f"Success! Deleted {deleted_count} duplicates.")
    print(f"You now have {len(seen_texts)} unique questions in the cloud!")

if __name__ == "__main__":
    cleanup_duplicates()
