import signal
import time
import math
import sys
import os
from .gameState import GameState

# Register an handler for the timeout
def timeOutHandler(signum, frame):
    raise TimeOutException()


class Player:
    ''' Class encapsulating the artificial intelligence, making the interface between the latter and a game
    inputs:
        - brain: the artificial intelligence. It must implement
                * a method "play" taking a gameState and returning one of the reachable gameState
                * the method __str__ defining the name of the ai
        - isWhite: true if the player is the white one
    '''

    def __init__(self, processus, isWhite, timeLimit):        
        self.processus = processus
        self.isWhite = isWhite
        self.timeLimit = timeLimit
        self.computingTimes = [] # store the computing time for each move
        self.showTime = False
        self.discard_stdout = False
        self._name = None
        
    @property
    def name(self):
        return self._name if self._name is not None else "no name yet"
    @name.setter
    def name(self,name):
        assert isinstance(name,str), "name must be a string"
        self._name = name

    def sendline(self, message):
        self.processus.stdin.write(message.encode()+b'\n')
        self.processus.stdin.flush()

    def receiveline(self, timeout):
        if timeout>0:
            # signals only take an integer amount of seconds, so I have to ceil the time limit
            signal.signal(signal.SIGALRM, timeOutHandler)
            signal.alarm(math.ceil(timeout))
        try:
            return self.processus.stdout.readline().decode().strip()
        except TimeOutException:
            raise
        finally:
            signal.alarm(0)

    def initialize(self, game_message, rules_message, timeout):
        self.sendline(game_message)
        self.sendline(rules_message)
        self.sendline("PLAYER "+('white' if self.isWhite else 'black'))
        message = self.receiveline(timeout = timeout)
        title, name, alwaysSeeAsWhite = message.split(' ')
        if title.lower() != 'intro' : raise Exception("Unexpected message in initialization: "+message)
        self.name = name
        self.alwaysSeeAsWhite = alwaysSeeAsWhite.lower()=='true'

    def play(self, gameState):
        reverse = (not self.isWhite) and self.alwaysSeeAsWhite
        if reverse: gameState.reverse()

        self.sendline('PLAY {0} {1}'.format(gameState, self.timeLimit) )
        t1 = time.time()
        message = self.receiveline(timeout = math.ceil(1.1*self.timeLimit))
        length = time.time()-t1
        title, chosenStateString = message.split(' ')
        if title.lower() != 'decision' : raise Exception("Unexpected message in play: "+message)        
        chosenState = GameState.fromString(chosenStateString, gameState)

        self.computingTimes.append(length)

        if self.timeLimit and length>(self.timeLimit+0.01):
            raise TimeOutException(str(self)+' took too much time to make a decision : '+str(length)+' sec')
        if self.showTime:
            print(str(self)+" took "+'{:.3f}'.format(length)+"s to make a decision")

        if reverse: chosenState.reverse()
        return str(chosenState)

    def __str__(self):
        return ("White" if self.isWhite else "Black")+' ('+self.name+')'


# Unhandled exception leading to the game interuption
class TimeOutException(Exception):
    def __init__(self):
        pass
