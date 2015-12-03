import string
def alphanumeric(s):
    ev = string.whitespace+string.punctuation
    for e in ev:
        if e in s:
            print e
            return False

    return True
print alphanumeric("hello world_")
