import time
import gc

from .move import Move
from .gameState import GameState
from .player import Player, TimeOutException

class Game:
    '''A Game instance runs a game between two ias. It manages the game's progress and checks players actions.

    inputs:
        - ia1: the starting artificial intel
        - ia2: the other artificial intelligence
        - config: configuration dictionary for the game
        - rules: a dictionary of boolean defining pieces available moves
        - Nlimit: (default 150) the maximum number of simulation iterations

    outputs:
        - pdn: the Portable Draught Notation summary of the game
    '''

    defaultConfig = {   'nRows': 8,
                        'nPieces': 12,
                        'whiteStarts':True }

    CheckersRules = {   'menCaptureBackward':False,
                        'kingsCanFly':False,
                        'menMustStop':True,
                        'noCaptureMax': 16 }

    InternatRules = {   'menCaptureBackward':True,
                        'kingsCanFly':True,
                        'menMustStop':False,
                        'noCaptureMax': 25 }

    defaultRules = CheckersRules

    def checkConfig(self, config, Nlimit, rules):
        for key in Game.defaultConfig:
            if key not in config: config[key] = Game.defaultConfig[key]
        for key in Game.defaultRules:
            if key not in rules: rules[key] = Game.defaultRules[key]

        assert config['nRows']%2==0, 'The number of rows ust be a multiple of 2'
        assert config['nPieces']>0, 'The number of pieces must be positive'
        assert rules['noCaptureMax']>0 , 'The number of maximum successive non-capturing moves before Draw must be positive'

        if not Nlimit: Nlimit = 2*config['nPieces']*config['noCaptureMax']
        assert Nlimit>0, 'The number of maximum simulation steps must be positive'
        self.Nlimit = Nlimit
        self.config = config

    def __init__(self, ia1, timeLimit1, ia2, timeLimit2, config = {}, , rules = {}, Nlimit = None):
        self.checkConfig(config, Nlimit, rules)
        self.gameState = GameState(self.config)
        self.whiteStarts = self.config['whiteStarts']
        self.noCaptureMax = self.config['noCaptureMax']
        self.player1 = Player(self.whiteStarts, ia1, timeLimit1)
        self.player2 = Player(not self.whiteStarts, ia2, timeLimit2)

        self.displayLevel = 0
        self.pause = 0
        self.log = ""
        self.status = {'success':False, 'draw':False, 'winner':None, 'playerError':None, 'errorID':None}

    def init_logs(self):
        self.addToLog("Beginning of the game")
        self.addToLog(str(self.player1)+ ' (starts) has '+str(self.player1.timeLimit)+' secs/turn to play')
        self.addToLog(str(self.player2)+ ' has '+str(self.player1.timeLimit)+' secs/turn to play')
        self.logState()

    def runGame(self):
        # setup
        self.init_logs()
        pdnMoves = ""
        result = None
        startTime = time.ctime()
        time.sleep(self.pause)
        t = time.time() + self.pause

        # shortcut variables to acces faster white and black players
        whitePlayer = self.player1 if self.player1.isWhite else self.player2
        blackPlayer = self.player2 if self.player1.isWhite else self.player1


        for n in range(self.Nlimit):
            player = whitePlayer if self.gameState.isWhiteTurn else blackPlayer
            playerNumber = 1 if player is self.player1 else 2

            # Check whether the game is ended
            possibleMoves = self.gameState.findPossibleMoves()
            possibleStates = self.gameState.findNextStates()
            if not possibleMoves:
                result = '0-1' if player is self.player1 else '1-0'
                self.status['success'] = True
                self.status['winner'] = 3 - playerNumber
                self.addToLog('End of Game !',1)
                break
            self.logChoices(possibleMoves)

            time.sleep(max(0, t-time.time()))
            t = time.time() + self.pause

            # make the player play
            try:
                chosenState = player.play( self.gameState.copy() )
            except TimeOutException as exc:
                self.status['playerError'] = playerNumber
                self.status['errorID'] = 'T0'
                self.addToLog(exc.message, 0)
                return
            except Exception as e:
                self.status['playerError'] = playerNumber
                self.status['errorID'] = 'Unknown'
                self.addToLog(e.message, 0)
                return

            # check whether the answer is valid
            move = None
            for m in possibleMoves:
                state = self.gameState.doMove(m, inplace = False)
                if chosenState == str(state):
                    move = m
                    self.gameState = state
                    break
            if not move:
                self.status['playerError'] = playerNumber
                self.status['errorID'] = 'IM'
                self.addToLog('Invalid move from '+str(player), 0)
                return

            # log the game
            self.logCompuTime(player.computingTimes[-1])
            self.logState()
            if player is self.player1: pdnMoves += str(n//2+1)+"."
            pdnMoves += move.toPDN()+" "

            # Check if it is a Draw
            if self.gameState.noCaptureCounter >= self.noCaptureMax:
                result = '1/2-1/2'
                self.status['success'] = True
                self.status['draw'] = True
                self.addToLog('Draw',1)
                break

            gc.collect()

        # If the simulation stops before the game ends
        if not self.status['success']:
            self.status['errorID'] = 'MAX'
            self.addToLog('The game could not end within '+str(self.Nlimit)+' steps')
            return

        # create the PDN of the game
        self.pdn = self.makePDN(startTime, pdnMoves, result)
        self.log +="\n#PDN#\n"+self.pdn

### End of runGame


    stateDisplayLevel = 1
    choiceDisplayLevel = 2
    decisionDisplayLevel = 2

    def addToLog(self, txt, displayLevel = 1):
        self.log += txt+'\n'
        if self.displayLevel >= displayLevel:
            print(txt)

    def logState(self):
        self.addToLog(self.gameState.toDisplay(True), Game.stateDisplayLevel)

    def logChoices(self, possibleMoves):
        recap = "Possible moves :\n"
        for m in possibleMoves:
            recap += m.toPDN()+"\n"
        self.addToLog(recap, Game.choiceDisplayLevel)

    def logCompuTime(self,t):
        self.addToLog("Computing time : "+str(t)+" sec(s)", Game.choiceDisplayLevel)

    def makePDN(self, startTime, pdnMoves, result):
        # shortcut variables to acces faster white and black players
        whitePlayer = self.player1 if self.player1.isWhite else self.player2
        blackPlayer = self.player2 if self.player1.isWhite else self.player1

        pdn  = '[Event "IN104 CS Project"]\n'
        pdn += '[Site "ENSTA ParisTech, Palaiseau, FRA"]\n'

        gameType  = '[GameType “21,'
        gameType += 'W' if self.whiteStarts else 'B'
        gameType += (','+str(self.gameState.boardState.nRows))*2+','
        gameType += 'N2,0”] {Whites begin}\n' if self.whiteStarts else 'N1,0”] {Blacks begin}\n'
        pdn += gameType
        pdn += '[Date "'+startTime+'"]\n'
        pdn += '[Round "?"]\n'
        pdn += '[White "'+whitePlayer.name()+'"]\n[WhiteType "Program"]\n'
        pdn += '[Black "'+blackPlayer.name()+'"]\n[BlackType "Program"]\n'

        pdn += '[Result "'+result+'"]'
        if result=='1-0':
            pdn += ' {'+str(self.player1)+' wins}'
        elif result=='0-1':
            pdn += ' {'+str(self.player2)+' wins}'

        pdn += '\n[WhiteTime "'+str(sum(whitePlayer.computingTimes))+'"]\n'
        pdn += '[BlackTime "'+str(sum(blackPlayer.computingTimes))+'"]\n\n'
        pdn += pdnMoves+' '+result+' *'+'\n'
        return pdn
