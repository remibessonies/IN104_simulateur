from .cpp.boardState import BoardState

class GameState:
    ''' The GameState gathers the state of the board plus some auxilliary info like whose turn to play and info to know if it is a draw '''

    def __init__(self, config = None, rules = None):
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

    def doMove(self, move, inplace = False):
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
        self.boardState.reverse()
        self.isWhiteTurn = not self.isWhiteTurn
        return self

    def __str__(self):
        s = "W" if self.isWhiteTurn else "B"
        return s+str(self.boardState)+str(self.noCaptureCounter)


    def toDisplay(self, showBoard = False):
        s = self.boardState.toDisplay(showBoard)+'\n'
        if self.isWhiteTurn:
            s += "White's turn to play."
        else:
            s += "Black's turn to play."
        return s

    def display(self, showBoard = False):
        print(self.toDisplay(showBoard))
