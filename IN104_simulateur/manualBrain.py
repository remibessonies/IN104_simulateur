import sys
import time
from .gameState import GameState
from .move import Move
from .player import TimeOutException

class ManualBrain:

    def __init__(self):
        print("Please enter your name")
        self.name = sys.stdin.readline()[0:-1]
        self.alwaysSeeAsWhite = False

    def play(self, gameState, timeLimit):
        possibleMoves = gameState.findPossibleMoves()
        print(gameState.toDisplay(True))
        print("Authorized moves : ")
        for m in possibleMoves: print(m.toPDN())
        
        string = ""
        while True:
            try:
                print("Please enter a move")
                string = sys.stdin.readline()[0:-1]
                if string not in [m.toPDN() for m in possibleMoves]: raise Exception
                move = Move.fromPDN(string)
                choice = gameState.doMove(move, inplace = False)
                break
            except TimeOutException as e:
                print('Sorry, you took to much time to think !')
                raise e
            except Exception:
                print(string+' is an invalid move !')

        return choice


    def __str__(self):
        return self.name
