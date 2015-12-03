#!/usr/bin/python
'''
Description:

Write a function called validParentheses that takes a string of parentheses, and determines if the order of the parentheses is valid. validParentheses should return true if the string is valid, and false if it's invalid.

Examples: 
validParentheses( "()" ) => returns true 
validParentheses( ")(()))" ) => returns false 
validParentheses( "(" ) => returns false 
validParentheses( "(())((()())())" ) => returns true 
All input strings will be nonempty, and will only consist of open parentheses '(' and/or closed parentheses ')'

Test case

Test.assert_equals(valid_parentheses("  ("),False)
Test.assert_equals(valid_parentheses(")test"),False)
Test.assert_equals(valid_parentheses(""),True)
Test.assert_equals(valid_parentheses("hi())("),False)
Test.assert_equals(valid_parentheses("hi(hi)()"),True)
'''
#solution
def valid_parentheses(string):
    #your code here
    if not string:
        return True
    if string.count("(") == string.count(")") and string[-1] != '(':
        return True
    else:
        return False
