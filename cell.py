from enum import Enum

class Color(Enum):
    ''' This enumeration represents the possible colors of pieces and by extensions the two players '''
    Black = False
    White = True
    
    def __invert__(self): # overload the ~ unary operator
        return Color(not self.value)
    
    def __str__(self):
        return self.name

   
class Cell(Enum):
    ''' This enumeration represents the possible states of a cell on the board '''
    empty = (None,False)
    w = (Color.White,False)
    W = (Color.White,True)
    b = (Color.Black,False)
    B = (Color.Black,True)
            
            
    def color(self):
        return self.value[0]  
        
    def isWhite(self):
        return self is Cell.w or self is Cell.W          
        
    def isBlack(self):
        return self is Cell.b or self is Cell.B     
      
    def isMan(self):
        return self is Cell.w or self is Cell.b   
      
    def isKing(self):
        return self.value[1]        
    
    def invertColor(self):
        return Cell.empty if self is Cell.empty else Cell( (~self.color(), self.isKing() ) )
        
    def promoted(self):
        return Cell.empty if self is Cell.empty else Cell( (self.color(), True) )
        
    def __str__(self):
        if self is Cell.empty: 
            return '.'
        else:
            r = self.name
        return r
        
