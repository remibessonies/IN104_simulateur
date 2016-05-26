from cython.operator cimport dereference as deref, preincrement as inc
from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector

from .move cimport *
from .boardState cimport *

cdef class GameState:
    ''' The GameState gathers the state of the board plus some auxilliary info like whose turn to play and info to know if it is a draw '''

    cdef BoardState boardState
    cdef bool isWhiteTurn
    cdef int noCaptureCounter

    property isWhiteTurn:
        def __get__(self): return self.isWhiteTurn

    property noCaptureCounter:
        def __get__(self): return self.noCaptureCounter

    property boardState:
        def __get__(self): return self.boardState


    def __cinit__(self, config = None, rules = None):
        if config:
            if not rules: raise Exception("You must provide a configuration AND rules")
            self.boardState = BoardState(config, rules)
            self.isWhiteTurn = config['whiteStarts']
            self.noCaptureCounter = 0

    def copy(self):
        copy = GameState()
        copy.boardState = self.boardState.copy()
        copy.noCaptureCounter = self.noCaptureCounter
        copy.isWhiteTurn = self.isWhiteTurn
        return copy

    def findPossibleMoves(self):
        return self.boardState.findPossibleMoves(self.isWhiteTurn)

    def doMove(self, Move move, inplace = False):
        if inplace:
            gs = self
        else:
            gs = GameState()
            gs.boardState = self.boardState.copy()
        gs.boardState.doMove(move)
        gs.noCaptureCounter = 0 if move.isCapture() else self.noCaptureCounter+1
        gs.isWhiteTurn = not self.isWhiteTurn
        return gs

    def findNextStates(self):
        moves = self.findPossibleMoves()
        nextStates = []
        for move in moves:
            nextStates.append( self.doMove(move, inplace = False) )
        return nextStates

    def reverse(self):
        self.boardState.cBoardState.reverse()
        self.isWhiteTurn = not self.isWhiteTurn
        return self

    def __str__(self):
        cdef string s
        s = string(b"W") if self.isWhiteTurn else string(b"B")
        s.append(self.boardState.cBoardState.toString())
        return s.decode('UTF-8')+str(self.noCaptureCounter)


    def toDisplay(self, showBoard = False):
        s = self.boardState.toDisplay(showBoard)+'\n'
        if self.isWhiteTurn:
            s += "White's turn to play."
        else:
            s += "Black's turn to play."
        return s

    def display(self, showBoard = False):
        print(self.toDisplay(showBoard))
