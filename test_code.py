#!/usr/bin/env python3
"""Test file with various code issues for BRIGADE testing"""

import os

def unsafe_eval(user_input):
    # Security issue: eval with user input
    result = eval(user_input)
    return result

def file_leak(filename):
    # Resource leak: file not closed
    f = open(filename, 'r')
    content = f.read()
    return content

def style_issues(value):
    # Style issue: != None instead of 'is not None'
    if value != None:
        return True
    return False

def division_risk(a, b):
    # Potential division by zero
    return a / b

def main():
    # Multiple issues in one function
    user_code = input("Enter code: ")
    result = unsafe_eval(user_code)
    
    data = file_leak("config.txt")
    
    if style_issues(result):
        print("Result is valid")
    
    calc = division_risk(10, 0)  # Will crash
    print(calc)

if __name__ == "__main__":
    main()
