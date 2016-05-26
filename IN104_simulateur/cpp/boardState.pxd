from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair

from .move cimport *

cdef extern from "CBoardState.h" namespace "game":
    cdef cppclass CBoardState:
        int nRows, nPieces, nCells

        CBoardState() except +
        CBoardState(int, int, bool, bool, bool) except +
        CBoardState(CBoardState&) except +

        void reverse()
        string toString()

        bool isValidIndex(int)
        bool isValidRC(int, int)
        int RCtoIndex(int, int)
        pair[int,int] indexToRC(int)
        
        char getCell(int, int)
        vector[char] getCells()
        void setCell(int, char)
        void setCell(int, int, char)

        vector[CCaptureMove*] tryJumpFrom(int)
        vector[CSimpleMove*] tryMoveFrom(int)
        vector[CMove*] findPossibleMoves(bool)
        void doMove(CMove& m) except +


cdef class BoardState:
    cdef CBoardState* cBoardState      # hold a C++ instance which we're wrapping
    cdef debug
