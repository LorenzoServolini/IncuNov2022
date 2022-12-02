def test_function(a,b):
    """ Why result1 is None? :(
    """
    result = a*b
    print('Result: {0}'.format(result))
    return result # Because there was not the return statement :)

result1 = test_function(2,4)
print(result1)

#######################################

def test_function2(a,b):
    """ Why do we have only 15 instead of Result: 15 as well? :(
    """
    result = a*b
    print('Result: {0}'.format(result)) # Due to the wrong order of the code :)
    return result

result2 = test_function2(3,5)
print(result2)