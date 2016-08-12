import signal
import time
import math
import sys
import os

# Register an handler for the timeout
def timeOutHandler(signum, frame):
    raise TimeOutException()


class StreamPlayer:
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

    def sendline(self, message):
        print(message, file=self.processus.stdin)

    def receiveline(self, timeout):
        if timeout>0:
            # signals only take an integer amount of seconds, so I have to ceil the time limit
            signal.signal(signal.SIGALRM, timeOutHandler)
            signal.alarm(math.ceil(timeout))
        try:
            return self.processus.stdout.readline().decode()
        except TimeOutException:
            raise
        finally:
            signal.alarm(0)

    def initialize(self, game_message, rules_message, timeout):
        self.sendline(game_message)
        self.sendline(rules_message)
        self.sendline("PLAYER "+('white' if self.isWhite else 'black'))
        (self.name, self.alwaysSeeAsWhite) = self.receiveline(timeout = timeout)


    def play(self, gameState):
        reverse = (not self.isWhite) and self.alwaysSeeAsWhite
        if reverse: gameState.reverse()

        self.sendline('PLAY '+str(gamestate)+' '+self.timeLimit)
        t1 = time.time()
        chosenState = self.receiveline()
        length = time.time()-t1

        self.computingTimes.append(length)

        if self.timeLimit and length>(self.timeLimit+0.01):
            raise TimeOutException(str(self)+' took too much time to make a decision : '+str(length)+' sec')
        if self.showTime:
            print(str(self)+" took "+'{:.3f}'.format(length)+"s to make a decision")

        if reverse: chosenState.reverse()
        return str(chosenState)

    def name(self):
        try: return self.name
        except: returnt "no name yet"

    def __str__(self):
        return ("White" if self.isWhite else "Black")+' ('+self.name()+')'


# Unhandled exception leading to the game interuption
class TimeOutException(Exception):
    def __init__(self):
        pass
