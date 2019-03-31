import signal
import time
import math
import sys
import os

# Register an handler for the timeout
def playTimeOutHandler(signum, frame):
    raise TimeOutException("Player takes too long to make a decision.")

USE_SIGNAL = hasattr(signal, 'SIGALRM')
if USE_SIGNAL: signal.signal(signal.SIGALRM, playTimeOutHandler)


class Player:
    ''' Class encapsulating the artificial intelligence, making the interface between the latter and a game
    inputs:
        - brain: the artificial intelligence. It must implement
                * a method "play" taking a gameState and returning one of the reachable gameState
                * the method __str__ defining the name of the ai
        - isWhite: true if the player is the white one
    '''

    def __init__(self, isWhite, brain, timeLimit=None):
        self.isWhite = isWhite
        assert brain, "Player needs a brain !"
        assert timeLimit is None or float(timeLimit) == timeLimit
        self.brain = brain
        self.timeLimit = timeLimit
        self.computingTimes = [] # store the computing time for each move
        self.showTime = False
        self.discard_stdout = False
        try:
            self.alwaysSeeAsWhite = self.brain.alwaysSeeAsWhite
        except:
            self.alwaysSeeAsWhite = True


    def play(self, gameState):
        reverse = (not self.isWhite) and self.alwaysSeeAsWhite
        if reverse: gameState.reverse()

        if USE_SIGNAL and self.timeLimit and self.timeLimit>0:
            # signals only take an integer amount of seconds, so I have to ceil the time limit
            signal.alarm(math.ceil(self.timeLimit+0.01))

        try:
            if self.discard_stdout: sys.stdout = open(os.devnull, "w")
            t1 = time.time()
            chosenState = self.brain.play(gameState, self.timeLimit)
            length = time.time()-t1
        except Exception as e:
            raise e
        finally:
            sys.stdout = sys.__stdout__

        if USE_SIGNAL: signal.alarm(0)

        self.computingTimes.append(length)

        if self.timeLimit and length>(self.timeLimit+0.01):
            raise TimeOutException(str(self)+' took too much time ('+str(length)+' s) to make a decision. Authorized time : '+str(self.timeLimit))
        if self.showTime:
            print(str(self)+" took "+'{:.3f}'.format(length)+"s to make a decision")

        if reverse: chosenState.reverse()
        return str(chosenState)


    def name(self):
        return str(self.brain)

    def __str__(self):
        return ("White" if self.isWhite else "Black")+' ('+self.name()+')'


# Unhandled exception leading to the game interuption
class TimeOutException(Exception):
    def __init__(self, message):
        self.message = message
