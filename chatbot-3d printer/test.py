import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock
from main import app

client = TestClient(app)

class TestMainRoutes(unittest.TestCase):

    #User Login Endpoint (/)
    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    #User Login Handler Endpoint (/login)
    @patch('main.authenticate_customer')
    def test_login_valid_credentials(self, mock_auth):
        mock_auth.return_value = {"_id": "123", "name": "John"}
        response = client.post("/login", data={"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)

    # @patch('main.authenticate_customer')
    # def test_login_invalid_credentials(self, mock_auth):
    #     mock_auth.return_value = False
    #     response = client.post("/login", data={"username": "baduser", "password": "badpass"})
    #     self.assertNotEqual(response.status_code, 200)

    #Chat Endpoint (/chat/{user_id})-------------------------------------------
    def setUp(self):
        # Patch the get_user_by_id method and set it as an instance variable so it can be accessed in other methods
        self.get_user_patch = patch('main.get_user_by_id')
        self.mock_get_user = self.get_user_patch.start()
        # Define a default mock user
        self.mock_user = {
            "_id": "64ef4efb6087a84dc1ff412c",
            "customer_name": "Eric",
            "chat_sessions": [] 
        }

    def tearDown(self):
        # Stop the patch after the test case finishes
        self.get_user_patch.stop()

    def test_chat_endpoint_valid_user(self):
        # Set the return value of the mock method for this scenario
        self.mock_get_user.return_value = self.mock_user
        response = client.post(f"/chat/{self.mock_user['_id']}")
        self.assertEqual(response.status_code, 200)

    def test_chat_endpoint_invalid_user(self):
        # Set the return value of the mock method for this scenario
        self.mock_get_user.return_value = None
        response = client.post("/chat/invalid_id")
        self.assertEqual(response.status_code, 404)

    #Chat Submission Endpoint (/chat/{user_id}/submit)--------------------------
    @patch('main.chat_with_bot')
    @patch('main.log_message')
    def test_chat_submission(self, mock_log, mock_gpt):
        mock_log.return_value = {"message": "Logged"}
        mock_gpt.return_value = "Response from GPT"
        response = client.post("/chat/123/submit", data={"user_message": "Hello", "session_id": "456"})
        self.assertEqual(response.json(), {"message": "Response from GPT"})
    
    # Failed Chat Submission due to "logging failure"
    @patch('main.chat_with_bot')
    @patch('main.log_message')
    def test_chat_submission_failed_logging(self, mock_log, mock_gpt):
        mock_gpt.return_value = "Response from GPT"
        mock_log.side_effect = Exception("Logging Failure") # Simulate logging failure
        response = client.post("/chat/123/submit", data={"user_message": "Hello", "session_id": "456"})
        self.assertEqual(response.status_code, 200)
    

    #Start New Session Endpoint (/start-session/{user_id})----------------------
    @patch('main.start_new_chat_session')
    def test_start_new_session(self, mock_start_session):
        mock_start_session.return_value = {"session_id": "789"}
        response = client.post("/start-session/123")
        self.assertEqual(response.json(), {"session_id": "789"})
    
    # Failed Start New Session
    @patch('main.start_new_chat_session')
    def test_failed_start_new_session(self, mock_start_session):
        mock_start_session.side_effect = Exception("Session Start Failure") # Simulate session start failure
        response = client.post("/start-session/123")
        self.assertEqual(response.status_code, 500)

    #Delete Session Endpoint (/delete-session/{user_id}/{session_id})------------
    @patch('main.delete_session')
    def test_delete_session(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/delete-session/123/456")
        self.assertEqual(response.json(), {"message": "Session deleted successfully"})
    
    # Failed Delete Session
    @patch('main.delete_session')
    def test_failed_delete_session(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/delete-session/123/456")
        self.assertEqual(response.status_code, 500)

    #   Get Session Endpoint (/get-session/{user_id}/{session_id})----------------
    @patch('main.get_messages_from_database')
    def test_get_session(self, mock_get_session):
        mock_messages = [{"sender": "user", "content": "Hello", "timestamp": "2023-09-10"}]
        mock_get_session.return_value = mock_messages
        response = client.get("/get-session/123/456")
        self.assertEqual(response.json(), mock_messages)
    
    ## Failed Get Session
    @patch('main.get_messages_from_database')
    def test_failed_get_session(self, mock_get_session):
        mock_get_session.return_value = None
        response = client.get("/get-session/123/456")
        self.assertEqual(response.status_code, 404)
    
    #  post to store feedback  ("/feedback/{user_id}/{session_id}/{msg_id}/{fb_message}")----------------
    @patch('main.log_feedback')
    def test_log_feedback(self, mock_log_feedback):
        mock_log_feedback.return_value = True
        response = client.post("/feedback/123/456/2/[]")
        self.assertEqual(response.json(), {"message": "Submit successfully"})
    
    ## Failed store feedback
    @patch('main.log_feedback')
    def test_failed_log_feedback(self, mock_log_feedback):
        mock_log_feedback.return_value = None
        response = client.post("/feedback/123/456/2/[]")
        self.assertEqual(response.status_code, 500)

    #   post to store rate (/rate/{user_id}/{session_id}/{msg_id}/{rate})----------------
    @patch('main.log_rate')
    def test_log_rate(self, mock_log_rate):
        mock_log_rate.return_value = True
        response = client.post("/rate/123/456/2/up")
        self.assertEqual(response.json(), {"message": "Rate successfully"})
    
    ## Failed store rating 
    @patch('main.log_rate')
    def test_failed_log_rate(self, mock_log_rate):
        mock_log_rate.return_value = False
        response = client.post("/rate/123/456/2/up")
        self.assertEqual(response.status_code, 500)

#-------------------------------------------------------------------------------------------
# from unittest.mock import patch

# class TestDatabaseFunctions(unittest.TestCase):

#     @patch("db.authenticate_customer")
#     def test_authenticate_customer(self, mock_authenticate):
#         # Mocking the return value
#         mock_authenticate.return_value = {"_id": "123", "name": "John"}

#         result = authenticate_customer("john@example.com", "password")
#         self.assertEqual(result, {"_id": "123", "name": "John"})


if __name__ == "__main__":
    unittest.main()