# distutils: language = c++
# distutils: sources = cpp/CBoardState.cpp cpp/Pieces.cpp cpp/CMove.cpp
from libcpp cimport bool
from libcpp.string cimport string
from libcpp.pair cimport pair
from libcpp.vector cimport vector
from libcpp.list cimport list
from cython.operator cimport dereference as deref, preincrement as inc
        
cdef extern from "CBoardState.h" namespace "game":
    cdef cppclass CBoardState:
        int nRows, nPieces, nCells
        
        CBoardState() except +
        CBoardState(int, int) except +
        CBoardState(CBoardState&) except +
        
        vector[char] getCells()
        void reverse()
        string toString()
        
        bool isValidIndex(int)
        bool isValidRC(int, int)
        int RCtoIndex(int, int)
        pair[int,int] indexToRC(int)
        char getCell(int, int)
        void setCell(int, char)
                
        vector[CCaptureMove*] tryJumpFrom(int)
        vector[CSimpleMove*] tryMoveFrom(int)
        vector[CMove*] findPossibleMoves(bool)
        void doMove(CMove& m) except +


cdef extern from "CMove.h" namespace "game":
    cdef cppclass CMove:  
        list[int] getCells()
        int len()  
        bool isCapture()
        string toPDN()
        
    cdef cppclass CCaptureMove(CMove):
        CCaptureMove() except +   
        CCaptureMove(int) except +
        void push_back(int) 
        
    cdef cppclass CSimpleMove(CMove):
        CSimpleMove() except +  
        CSimpleMove(int, int) except + 



cdef class GameState:
    ''' The GameState gathers the state of the board plus some auxilliary info like whose turn to play and info to know if it is a draw '''
    
    cdef BoardState boardState 
    cdef bool nextColor
    cdef int noCaptureCounter 
    
    property nextColor:
        def __get__(self): return self.nextColor        
        
    property noCaptureCounter:
        def __get__(self): return self.noCaptureCounter
        
    property boardState:
        def __get__(self): return self.boardState
        
    
    def __cinit__(self, config = None):
        if config:
            self.boardState = BoardState(config['nRows'], config['nPieces'])
            self.nextColor = config['startingColor']
            self.noCaptureCounter = 0
          
    def copy(self):
        copy = GameState()
        copy.boardState = self.boardState.copy()
        copy.noCaptureCounter = self.noCaptureCounter
        copy.nextColor = self.nextColor
        return copy   
                            
    def findPossibleMoves(self):
        cdef vector[CMove*] cMoves = self.boardState.cBoardState.findPossibleMoves(self.nextColor)
        return [Move.wrap(m) for m in cMoves]
           
    def doMove(self, Move move, inplace = False):   
        cdef CMove* cMove = move.cMove       
        if inplace:
            gs = self
        else:
            gs = GameState()
            gs.boardState = self.boardState.copy()    
        gs.boardState.cBoardState.doMove(deref(cMove)) 
        gs.noCaptureCounter = 0 if cMove.isCapture() else self.noCaptureCounter+1
        gs.nextColor = not self.nextColor
        return gs    
        
    cdef GameState doCMove(self, CMove& cMove):
        gs = GameState()
        gs.boardState = self.boardState.copy()     
        gs.boardState.cBoardState.doMove(cMove)       
        gs.noCaptureCounter = 0 if cMove.isCapture() else self.noCaptureCounter+1
        gs.nextColor = not self.nextColor
        return gs
        
      
    def findNextStates(self):
        cdef vector[CMove*] cMoves = self.boardState.cBoardState.findPossibleMoves(self.nextColor)      
        nextStates = {}
        for cMove in cMoves:
            gs = self.doCMove(deref(cMove))
            nextStates[ str(gs) ] = gs
            del cMove 
        return nextStates     

    def getStateMoveDict(self):
        cdef vector[CMove*] cMoves = self.boardState.cBoardState.findPossibleMoves(self.nextColor)      
        nextStates = {}
        for cMove in cMoves:
            gs = self.doCMove(deref(cMove))
            nextStates[ str(gs) ] = Move.wrap(cMove)
        return nextStates  

                  
    def reverse(self):
        self.cGameState.reverse()
        return self
      
    def __str__(self):
        return self.cGameState.toString().decode('UTF-8')
        

    def toDisplay(self, showBoard = False):
        s = self.boardState.toDisplay(showBoard)+'\n'
        if self.nextColor:
            s += "White's turn to play."
        else:
            s += "Black's turn to play."        
        return s
        
    def display(self, showBoard = False):
        print(self.toDisplay(showBoard)) 


cdef class BoardState:
    '''
    This class is a Pyhton interface (front-end) for the C++ backend of CBoardState.
    It also contains some non-critic functions (whose performance is not critical) like displaying the board
    '''
    cdef CBoardState* cBoardState      # hold a C++ instance which we're wrapping
    cdef debug
    
    property debug:
        def __get__(self): return self.debug
        def __set__(self, bool b): self.debug = b
        
    property nRows:
        def __get__(self): return self.cBoardState.nRows
        
    property nCells:
        def __get__(self): return self.cBoardState.nCells
        
    property nPieces:
        def __get__(self): return self.cBoardState.nPieces
        
    property cells:
        def __get__(self): return self.cBoardState.getCells()
        
    
    def __cinit__(self, nRows=None, nPieces=None):
        self.debug = False
        if nPieces:
            self.cBoardState = new CBoardState(nRows, nPieces)
           
    def __dealloc__(self):
        del self.cBoardState
        
    def copy(self):
        copy = BoardState()
        copy.cBoardState = new CBoardState( deref(self.cBoardState) )
        return copy
        
    def reverse(self):
        self.cBoardState.reverse()
        return self      
        
    def __str__(self):
        return self.cBoardState.toString().decode('UTF-8')
         
    '''
    Checkers, converters, getters and setter
    '''       
    def isValidIndex(self, int i):
        return self.cBoardState.isValidIndex(i)
        
    def isValidRC(self, int r, int c):
        return self.cBoardState.isValidRC(r,c)
    
    def RCtoIndex(self, int r, int c):
        return self.cBoardState.RCtoIndex(r,c) 
        
    def indexToRC(self, int i):
        return self.cBoardState.indexToRC(i)
        
    def getCell(self, int r,int c):
        return chr(self.cBoardState.getCell(r, c))
                
    def setCell(self, i, cell):
        cdef char c = ord(str(cell)) # convert the Cell to string, then get the asci code (char value)
        self.cBoardState.setCell(i, c)        
        
    ''' 
    Core methods 
    '''
             
    def tryMoveFrom(self, int cellIndex):
        cdef vector[CSimpleMove*] cmoves = self.cBoardState.tryMoveFrom(cellIndex)
        return [Move.wrap(m) for m in cmoves]    
    
    def tryJumpFrom(self, int cellIndex):
        cdef vector[CCaptureMove*] cmoves = self.cBoardState.tryJumpFrom(cellIndex)
        return [Move.wrap(m) for m in cmoves]
        
    def findPossibleMoves(self, bool white):
        cdef vector[CMove*] cmoves = self.cBoardState.findPossibleMoves(white)
        return [Move.wrap(m) for m in cmoves]
    
    def doMove(self, Move move):
        cdef CMove* c = move.cMove
        self.cBoardState.doMove( deref(c) )
        return self        
            
       
    def findNextStates(self, bool white):
        moves = self.findPossibleMoves(white)
        nextStates = []
        for m in moves:
            nextStates.append( self.copy().doMove(m) )
        return nextStates
        
 

    '''
    Visualization methods
    '''
    def toDisplay(self, showBoard = False):
        ''' Return a string suitable for state visualization in text mode (like the one at the top of this file) 
        If showBard is True, then a board with cell indices is shown next to the state'''
        
        formater = '{0:3d}'
        nRows = self.cBoardState.nRows
        
        s = ","+('---'*nRows)+","
        if showBoard:
            s+= "    ,"+('---'*nRows)+","
        s +="\n"
        for r in range(nRows):
            s+='|'
            for c in range(nRows):
                if c%2 != r%2:
                    s+=' '+str(self.getCell(r,c))+' '
                else:
                    s+='   '
            s+='|'
            if showBoard:
                s+='    |'
                for c in range(nRows):
                    if c%2 != r%2:
                        s+=formater.format(self.RCtoIndex(r,c))
                    else:
                        s+='   '
                s+='|'
            
            s+='\n'
        s+= "'"+('---'*nRows)+"'" 
        if showBoard:
            s+= "    '"+('---'*nRows)+"'"
        return s  
        
    def display(self, showBoard = False):
        print(self.toDisplay(showBoard))

        
    def viewBoard(self):
        formater = '{0:3d}'
        nRows = self.cBoardState.nRows
        
        s = ","+('---'*nRows)+",\n"
        for r in range(nRows):
            s+='|'
            for c in range(nRows):
                if c%2 != r%2:
                    s+=formater.format(self.RCtoIndex(r,c))
                else:
                    s+='   '
            s+='|\n'            
        s+= "'"+('---'*nRows)+"'\n"        
        return s


        
cdef class Move:
    ''' A move is simply a list of cells which a piece passes by. 
    
    It can be either a CaptureMove or a SimpleMove. 
    These classes do not check whether the list of cells define a valid move'''
    
    cdef CMove* cMove
    
    def __cinit__(self):
        pass     
        
    def __dealloc__(self):
        del self.cMove
    
    @staticmethod
    cdef wrap(CMove* m):
        result = Move()
        result.cMove = m
        return result         
 
    def __len__(self):
        return self.cMove.len()       

    
    def isCapture(self):
        return self.cMove.isCapture()
    
    def toPDN(self):
        return self.cMove.toPDN().decode('UTF-8')
        
    @staticmethod
    def fromPDN(s):
        assert(s.rfind('x')>-1 or s.rfind('-')>-1)
        separator = 'x' if s.rfind('x')>-1 else '-'
        cdef vector[int] cells = [int(i) for i in s.split(separator)]
        assert(separator=='x' and len(cells)>=2 or len(cells)==2)
        
        move = Move()   
        cdef CSimpleMove* csmove
        cdef CCaptureMove* ccmove
        if separator=='-':
            csmove = new CSimpleMove(cells[0], cells[1])
            move.cMove = csmove
        else:
            ccmove = new CCaptureMove(cells[0])
            for k in range(1,len(cells)):
                ccmove.push_back(cells[k])
            move.cMove = ccmove
             
        return move