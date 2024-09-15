import unittest
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from db import(
    customers,
    get_user_by_id, 
    authenticate_customer, 
    start_new_chat_session, 
    log_message, 
    delete_session, 
    get_messages_from_database,
    log_rate,
    log_feedback
)

class MyTestCase(unittest.TestCase):
    # test_user = {
    #     "customer_id": 1,
    #     "customer_name": "Eric",
    #     "customer_email": "a@gmail.com",
    #     "customer_password": "123456",
    #     "chat_sessions": []
    # }
    # customers.insert_one(user_data)
    user_id = '64efcefb6087a84dc1ff412c'
    oid = ObjectId(user_id)
    user = customers.find_one({"_id": oid})
    user2 = customers.find_one({"customer_email": "a@gmail.com"})
        

    # get user----------------------------------------------
    def test_get_user_by_id(self):
        assert get_user_by_id(self.user_id) == self.user

    # # login auth------------------------------------------
    # ## success
    def test_authenticate_customer_success(self):
        assert authenticate_customer("a@gmail.com", "123456") == self.user2

    # ## fail
    def test_authenticate_customer_fail(self):
        assert authenticate_customer("a@gmail.com", "111111") == False

    # new chat section--------------------------------------
    ## invalid input
    # def test_start_new_chat_session_invalid_input(): 
    #     with assertRaises(Exception):
    #         start_new_chat_session("abc")

    ## user not found
    def test_start_new_chat_session_not_found(self): 
        assert start_new_chat_session("626bccb9697a12204fb22ea3") == {'error': 'User not found'}

    ## new section
    # def test_start_new_chat_session(self):
    #     new_session = {
    #         "session_id": str(ObjectId()),  # Using ObjectId as a unique session ID
    #         "start_timestamp": datetime.now().isoformat().replace('T', ' '),
    #         "chat_log": [
    #             {
    #                 "_id": str(ObjectId()),
    #                 "sender": "chatbot",
    #                 "content": "Asiga GPT: How can I help you?",
    #                 "timestamp": datetime.now().isoformat().replace('T', ' ')
    #             }
    #         ]
    #     }
    #     assert start_new_chat_session(self.user_id) == new_session

    # log msg-------------------------------------------------
    ## user not found
    def test_log_message_user_not_found(self): 
        assert log_message("626bccb9697a12204fb22ea3", "123", "x", "y") == {"error": "User not found"}

    ## invalid input
    def test_log_message_invalid_input(self): 
        assert log_message(self.user_id, "626bccb9697a12204fb22ea3", "x", "y") == {"error": "User not found"}

    # get msg-------------------------------------------------

    ## msg generated
    def test_get_messages_from_database(self):
        assert get_messages_from_database(self.user_id, "626bccb9697a12204fb22ea3") == []
        
    ## MongoDB error occurs
    def test_get_messages_from_database(self):
        assert get_messages_from_database("626bccb9697a12204fb22ea3", "626bccb9697a12204fb22ea3") == []

    # delete session------------------------------------------
    ## success
    def test_delete_session_success(self): 
        assert delete_session(self.user_id, "sessionid") == False

    ## fail
    def test_delete_session_fail(self): 
        assert delete_session("626bccb9697a12204fb22ea3", "sessionid") == False

    # log feedback and rating --------------------------------
    ## success log feedback
    def test_log_feedback(self): 
        assert log_feedback("651ba0002232ff86da87f4c3", "653214c5b7cd98f806c48a3c", "3", []) == True

    ## fail log fb
    def test_log_feedback_fail(self): 
        assert log_feedback("651ba0002232ff86da87f4c3", "653214c5b7cd98f806c48a3c", "2", []) == True

    ## success log rate
    def test_log_rate_success(self): 
        assert log_rate("651ba0002232ff86da87f4c3", "653214c5b7cd98f806c48a3c", "2", "up") == True

    ## fail log rate
    def test_log_rate_fail(self): 
        assert log_rate("651ba0002232ff86da87f4c3", "653214c5b7cd98f806c48a3c", "2", "down") == True

    

if __name__ == '__main__': 
    unittest.main()
