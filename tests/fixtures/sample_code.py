"""Sample code with issues for testing"""


def unsafe_eval(user_input):
    return eval(user_input)


def file_leak(filename):
    f = open(filename, "r")
    return f.read()


def style_issue(value):
    if value != None:
        return True
    return False
