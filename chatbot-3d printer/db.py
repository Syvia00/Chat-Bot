from datetime import datetime
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from pydantic import BaseModel
from typing import List, Dict, Any

# ***Change it to your own MongoDB URI
uri = "mongodb+srv://eric:123@asiga.tmcfs9q.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)


db = client['chat_db'] #database name 
customers = db['customers'] #collection name

def get_database():
    db = MongoClient(uri)
    return db.customers

#----------------------------------------
###  set seed my own data (hard code)
### *** I've already populated my database with seed data, so I've commented out this section. It's used to simulate interactions after connecting to existing users from the Asiga client.***

# def seed_data():
#     # Check if the user already exists
#     if not customers.find_one({"customer_email": "a@gmail.com"}):
#         user_data = {
#             "customer_id": 1,
#             "customer_name": "Eric",
#             "customer_email": "a@gmail.com",
#             "customer_password": "123456",
#             "chat_sessions": []
#         }
#         customers.insert_one(user_data)

# seed_data()
#------------------------------------------


#get user
def get_user_by_id(user_id):
    return customers.find_one({"_id": ObjectId(user_id)})

#get curr time
def get_readable_time():
    now = datetime.now()
    formatted_time = now.strftime('%Y/%m/%d %H:%M:%S')
    return formatted_time

#login auth
def authenticate_customer(email, password):
    user = customers.find_one({"customer_email": email})
    if user and user["customer_password"] == password:
        return user
    else:
        return False

#new chat session
def start_new_chat_session(user_id: str):
    # Get the user from the DB
    oid = ObjectId(user_id)
    user = customers.find_one({"_id": oid})

    if not user:
        return {"error": "User not found"}

    # Create a new session
    new_session = {
        "session_id": str(ObjectId()),  # Using ObjectId as a unique session ID
        "start_timestamp": get_readable_time(),
        "chat_log": [
            {
                "_id": str(ObjectId()),
                "sender": "chatbot",
                "content": "Asiga GPT: How can I help you?",
                "timestamp": get_readable_time(),
                "rate": "None",
                "feedback": "None"
            }
        ]
    }

    # Append this session to user's chat_sessions and save
    # user['chat_sessions'].append(new_session)

    # customers.save(user)

    # for mongodb with 4.2+ version
    db.customers.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"chat_sessions": new_session}}
    )

    return new_session

#when msg is sent or received
def log_message(user_id, session_id, sender, content):
    user = get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}

    message = {
        "sender": sender,
        "content": content,
        "timestamp": get_readable_time(),
        "rate": "None",
        "feedback": []
    }
    
    try:
        db.customers.update_one(
            {"_id": ObjectId(user_id), "chat_sessions.session_id": session_id},
            {"$push": {"chat_sessions.$.chat_log": {
                "sender": sender,
                "content": content,
                "timestamp": get_readable_time(),
                "rate": "None",
                "feedback": []
            }}}
        )
    except PyMongoError as e:
        print("MongoDB Error in log_message:", e)

    return message

#delete chat session
def delete_session(user_id: str, session_id: str) -> bool:
    """
    Deletes a chat session for a given user.

    :param user_id: User ID string.
    :param session_id: Session ID string.
    :return: True if deletion succeeded, False otherwise.
    """
    try:
        result = db.customers.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"chat_sessions": {"session_id": session_id}}}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        print("MongoDB Error in delete_session:", e)
        return False
    
#hist chat
def get_messages_from_database(user_id: str, session_id: str) -> List[Dict[str, Any]]:
    try:
        user_data = db.customers.find_one({"_id": ObjectId(user_id)})
        
        if not user_data:
            return []

        # Find the session by session_id
        for session in user_data.get("chat_sessions", []):
            if session["session_id"] == session_id:
                return session.get("chat_log", [])

        return []

    except Exception as e:
        print("Error in get_messages_from_database:", e)
        raise Exception("An error occurred while fetching messages from the database.") from e


#when feedback recieve
def log_feedback(user_id, session_id, msgId, content):
    user = get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}
    
    ## update feedback
    try:
        db.customers.update_one(
            {"_id": ObjectId(user_id), "chat_sessions.session_id": session_id},
            {"$push": {"chat_sessions.$.chat_log."+str(msgId)+".feedback": content}}
        )
        return True
        
    except PyMongoError as e:
        print("MongoDB Error in log_feedback:", e)
        return False


def log_rate(user_id, session_id, msgId, rate):
    user = get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}
    ## update rates
    try:
        db.customers.update_one(
            {"_id": ObjectId(user_id), "chat_sessions.session_id": session_id},
            {"$set": {"chat_sessions.$.chat_log."+str(msgId)+".rate": rate}}
        )
        return True
    except PyMongoError as e:
        print("MongoDB Error in log_rate:", e)
        return False