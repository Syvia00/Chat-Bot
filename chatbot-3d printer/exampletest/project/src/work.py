


def in_out():
    response = input("Hello, how can I help you: ")
    if response == "you can not help me":
        return "Ok, let me refer you forward."
    response = input("Ok I'll see what I can do - what is your name?")
    if response == "jack":
        return "Hello jack."
    elif response == "jill":
        return "Hello jill."
    elif response == "help":
        return "Same input twice"
    elif response == "null":
        return "ERROR - null"
    return "I don't know you... have a nice day!"


def unfinished_function(param_1, param_2):
    # This code is unfinished - perhaps as part of a concurrently developed user story
    # Alternatively, you are writing unit tests, and don't want dependencies from
    #   other functions, so you instead mock this function for the unit test
    # print("Returning None!")
    return None


# This function relies on the above function to work, but this function can
#   still be unit tested by mocking the return values of 'unfinished_function()'
def finished_function():
    x = 10
    y = 5
    ret_val = unfinished_function(x,y)
    print(ret_val)
    if ret_val == 50:
        return "multiplication"
    elif ret_val == 2:
        return "division"
    elif ret_val == 15:
        return "addition"
    elif ret_val == 5:
        return "subtraction"
    else:
        return "Math Error"

if __name__ == '__main__':
    print("Going to ask the user now!")
    print(in_out())