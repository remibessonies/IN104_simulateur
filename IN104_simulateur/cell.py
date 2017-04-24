''' This enumeration represents the possible states of a cell on the board '''
empty = 46
w = 119
W = 87
b = 98
B = 66

def isWhite(c):
    return c == w or c == W

def isBlack(c):
    return c == b or c == B

def isMan(c):
    return c == w or c == b

def isKing(c):
    return c == W or c == B

def invertColor(c):
    if c == empty: return empty
    return c + 42*(1-c%2) - 21

def promoted(c):
    assert(isMan(c))
    return c-32

def toString(c):
    return chr(c)
