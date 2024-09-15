import unittest
from unittest import mock
from unittest.mock import patch

import sys
sys.path.append("..")

from src.work import *



class Test_in_out(unittest.TestCase):

# Way of doing mock input for only input:
    # with patch('builtins.input', return_value="user_response_being_mocked"):
    #     self.assertEqual(in_out(), expected_function_return_value)
# i.e. if the user inputs "user_response_being_mocked", then the function
#      will return expected_function_return_value

# Way of doing mock input for multiple inputs in the same function:
    # p1 = "Prompt_inside_first_input()_function" # i.e. what goes in response = input("<here>"")
    # p2 = "Prompt_inside_second_input()_function"
    # mock.builtins.input = lambda prompt: "user_response_being_mocked_1" if prompt == p1 else ("user_response_being_mocked_2" if prompt == p2 else "user_response_being_mocked_3")
    # self.assertEqual(in_out(), "expected_function_return_value")
# If you have more input() statements, then you have to increase the size of the lambda
#   expression, with more nested __ if <cond1> else (__ if <cond2> else (__ if <cond3> else)) 
#   and so on https://www.geeksforgeeks.org/how-to-use-if-else-elif-in-python-lambda-functions/


    # Mocking input for only one 'input(...)'
    def test_in_out_no_help(self):
        with patch('builtins.input', return_value="you can not help me"):
            self.assertEqual(in_out(), "Ok, let me refer you forward.")


    # Mocking input for mulitple 'input(...)'-s
    def test_in_out_jack(self):
        original_input = mock.builtins.input
        p1 = "Hello, how can I help you: "
        p2 = "Ok I'll see what I can do - what is your name?"
        mock.builtins.input = lambda prompt: "Help" if prompt == p1 else ("jack" if prompt == p2 else "null")
        self.assertEqual(in_out(), "Hello jack.")
        mock.builtins.input = original_input
    

    def test_in_out_jill(self):
        original_input = mock.builtins.input
        p1 = "Hello, how can I help you: "
        p2 = "Ok I'll see what I can do - what is your name?"
        mock.builtins.input = lambda prompt: "Help" if prompt == p1 else ("jill" if prompt == p2 else "null")
        self.assertEqual(in_out(), "Hello jill.")
        mock.builtins.input = original_input


    def test_in_out_unknown(self):
        original_input = mock.builtins.input
        p1 = "Hello, how can I help you: "
        p2 = "Ok I'll see what I can do - what is your name?"
        mock.builtins.input = lambda prompt: "help" if prompt == p1 else ("unknown" if prompt == p2 else "null")
        self.assertEqual(in_out(), "I don't know you... have a nice day!")
        mock.builtins.input = original_input




class Test_finished_function(unittest.TestCase):

# Basic way of mocking functions: 
    # with patch('path_to_file.mocked_function_name', return_value=mocked_return_value):
        # self.assertEqual(tested_function_name(), expected_return_value)


    def test_finished_function_multiplication(self):
        with patch('src.work.unfinished_function', return_value=50):
            self.assertEqual(finished_function(), "multiplication")

    def test_finished_function_division(self):
        with patch('src.work.unfinished_function', return_value=2):
            self.assertEqual(finished_function(), "division")

    def test_finished_function_addition(self):
        with patch('src.work.unfinished_function', return_value=15):
            self.assertEqual(finished_function(), "addition")

    def test_finished_function_subtraction(self):
        with patch('src.work.unfinished_function', return_value=5):
            self.assertEqual(finished_function(), "subtraction")

    def test_finished_function_none_return(self):
        with patch('src.work.unfinished_function', return_value=None):
            self.assertEqual(finished_function(), "Math Error")

    def test_finished_function_none_bad_values(self):
        with patch('src.work.unfinished_function', return_value=999):
            self.assertEqual(finished_function(), "Math Error")




if __name__ == '__main__':
    unittest.main()
