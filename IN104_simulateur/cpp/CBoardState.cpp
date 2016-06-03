#include <iostream>
#include <stdlib.h>        // abs
#include <list>
#include "CBoardState.h"

namespace game {
    CBoardState::CBoardState() {}

    CBoardState::CBoardState(const int nR, const int nP, const bool menBack, const bool kingsFly, const bool menStop) {
        nRows = nR;
        nPieces = nP;
        nCells = nRows*nRows/2;

        menCaptureBackward = menBack;
        kingsCanFly = kingsFly;
        menMustStop = menStop;

        cells = std::vector<char>(nCells, '.');
        init();
    }

    CBoardState::CBoardState(const CBoardState& bs) {
        nRows = bs.nRows;
        nPieces = bs.nPieces;
        nCells = bs.nCells;
        menCaptureBackward = bs.menCaptureBackward;
        kingsCanFly = bs.kingsCanFly;
        menMustStop = bs.menMustStop;
        cells = std::vector<char>(bs.cells);
    }

    CBoardState::~CBoardState() {}

    void CBoardState::init(){
        for (int i = 0; i < nPieces; i++)
            cells[i] = Cell::b;
        for (int i = nPieces; i < nCells-nPieces; i++)
            cells[i] = Cell::empty;
        for (int i = nCells-nPieces; i < nCells; i++)
            cells[i] = Cell::w;
    }

    std::vector<char> CBoardState::getCells(){
        return cells;
    }

    void CBoardState::reverse(){
        char x;
        for (int i = 0; i < nCells/2; i++){
            x = cells[i];
            cells[i] = Cell::invertColor(cells[nCells-i-1]);
            cells[nCells-i-1] = Cell::invertColor(x);
        }
    }

    std::string CBoardState::toString(){
        return std::string(cells.begin(), cells.end());
    }

/*
Convertissors, checkers and getters
*/

    bool CBoardState::isValidIndex(const int i){
        return (0<=i && i<nCells);
    }

    bool CBoardState::isValidRC(const int r, const int c){
        return (0<=r && r<nRows) && (0<=c && c<nRows) && (r%2 != c%2);
    }

    int CBoardState::RCtoIndex(const int r, const int c){
        return r*(nRows/2) + c/2;
    }

    std::pair<int,int> CBoardState::indexToRC(const int i){
        int r = i/(nRows/2);
        std::pair<int,int> rc (r, 2*(i%(nRows/2)) + (r+1)%2 );
        return rc;
    }

    char CBoardState::getCell(const int i){
        if(!isValidIndex(i)){
            std::cout << "Non valid index : " << i << "\n";
            throw "Non valid index";
        }
        return cells[i];
    }

    char CBoardState::getCell(const int r, const int c){
        if(!isValidRC(r,c)){
            std::cout << "Non valid coordinates : " << r << ", " << c << "\n";
            throw "Non valid coordinates";
        }
        return cells[RCtoIndex(r,c)];
    }

    void CBoardState::setCell(const int i, const char c){
        if(!isValidIndex(i)) throw "Non valid coordinates";
        cells[i] = c;
    }

      void CBoardState::setCell(const int r, const int c, const char cell){
          if(!isValidRC(r,c)) throw "Non valid coordinates";
          cells[RCtoIndex(r,c)] = cell;
      }





    std::vector<CCaptureMove*> CBoardState::tryJumpFrom(const int cellIndex){
        char piece = cells[cellIndex];
        if (piece == Cell::empty) throw "Error, the starting position contains no piece";
        std::set<int> previousCaptures;
        std::vector<CCaptureMove*> possibleMoves = tryJumpFrom(cellIndex, cellIndex, piece, previousCaptures);
        return possibleMoves;
    }

    std::vector<CCaptureMove*> CBoardState::tryJumpFrom(const int cellIndex, const int initPos, const char piece, std::set<int>& previousCaptures){
//        Find capturing moves that a piece located at a given position.
//
//        Inputs:
//            - cellIndex : the piece's position on the board.
//            - initPos   : the initial pose of the piece
//            - piece     : the type of piece being moved
//        Output:
//            - moves: a list of valid variations. A variation is a list of jumps

        std::pair<int,int> rc0 = indexToRC(cellIndex);
        int r0 = rc0.first;
        int c0 = rc0.second;

        int tr_min = (r0>0  && (piece!=Cell::b || menCaptureBackward) ) ? -1 : 1;
        int tr_max = (r0<nRows-1 && (piece!=Cell::w || menCaptureBackward) ) ? 1 : -1; //authorize to move in positive row
        int magnitude = (kingsCanFly && Cell::isKing(piece)) ? nRows : 1;
        //std::cout << piece << " : trmin/trmax : " << tr_min << " / " << tr_max << std::endl;
        //std::cout << menCaptureBackward << " !! " << r0 << " / " << c0 << std::endl;

        //a list of Move objects that the piece can perform starting from this place (these moves do not include the starting point)
        std::vector<CCaptureMove*> possibleVariations;
        std::vector<CCaptureMove*> newVariations;

        int r2,c2, jumpPos, newPos;
        bool isWhite = Cell::isWhite(piece);
        char jumpedCell;
        for (int tr=tr_min; tr<=tr_max; tr+=2){
            for (int tc=-1; tc<=1; tc+=2){
                for (int k=1; k<=magnitude; ++k){
                    if( !isValidRC(r0+ k*tr, c0+ k*tc) ) break;
                    jumpPos = RCtoIndex(r0+ k*tr, c0+ k*tc);
                    jumpedCell = cells[jumpPos];
                    if( jumpedCell==Cell::empty ) continue;
                    if( Cell::isWhite(jumpedCell)==isWhite || previousCaptures.find(jumpPos) != previousCaptures.end() ) break;

                    // we have foundthe closest opponent piece to jump above
                    // we will search now all the landing possibilities (if there are)
                    for(int k2=1; k2<=magnitude; k2++){
                        r2 = r0+(k+k2)*tr;
                        c2 = c0+(k+k2)*tc;
                        if( !isValidRC(r2, c2) ) break;

                        newPos = RCtoIndex(r2,c2);
                        if( cells[newPos]==Cell::empty || newPos==initPos ){
                            // if this is a valid jump
                            if( menMustStop && !Cell::isKing(piece) && ((r2==0 && isWhite) || (r2==nRows-1 && !isWhite)) ){
                                // if a man has reached the last row, it has to stop and be crowned if the rules say so
                                possibleVariations.push_back( new CCaptureMove(newPos) );
                            }else{
                                std::set<int> newPreviousCaptures = std::set<int>(previousCaptures);
                                newPreviousCaptures.insert(jumpPos);
                                newVariations = tryJumpFrom(newPos, initPos, piece, newPreviousCaptures);
                                possibleVariations.insert(possibleVariations.end(), newVariations.begin(), newVariations.end());
                            }
                        }else{
                            // if the cell is not empty, then we cannot land here and farther. we stop the search
                            break;
                        }
                    }
                    // now that we have found the closest opponent piece in this direction, we must stop searching
                    break;

                }
            }
        }


//        if (debug){
//            print(tabs,'possible variations before taking the max :')
//            for move in possibleVariations:print(tabs, move.toPDN())
//            print()
//        }

        std::vector<CCaptureMove*> longestVariations;

        if(possibleVariations.size()>0){
            // Once we've gathered all possible variations from the four adjacent cells, we keep only the longest ones
            int currentMax = 0;
            int len;

            for (std::vector<CCaptureMove*>::iterator variation = possibleVariations.begin(); variation != possibleVariations.end(); ++variation){
                len = (*variation)->len();
                if (len > currentMax){
                    currentMax = len;
                    longestVariations.clear();
                }
                if (len >= currentMax){
                    //Then we insert the starting point at the beginning of all variations kept
                    (*variation)->push_front(cellIndex);
                    longestVariations.push_back(*variation);
                }
            }

        }else if(!previousCaptures.empty()){
            // if there is no move possible from this cellIndex and that there has been previous capture,
            // then it means cellIndex is the end of a move and we need to put it in the possible moves
            longestVariations.push_back( new CCaptureMove(cellIndex) );
        }

//        if self.debug:
//            print(tabs,'possible ends of the move :')
//            for move in moves:print(tabs, move.toPDN())
//            print()

        return longestVariations;
    }


    std::vector<CSimpleMove*> CBoardState::tryMoveFrom(const int cellIndex){
        char piece = cells[cellIndex];
        std::vector<CSimpleMove*> possibleMoves;
        if (piece==Cell::empty) throw "Error, the starting position contains no piece";

        std::pair<int,int> rc = indexToRC(cellIndex);
        int r = rc.first;
        int c = rc.second;

        int tr_min = (r>0  && piece!=Cell::b) ? -1 : 1;
        int tr_max = (r<nRows-1 && piece!=Cell::w) ? 1 : -1; //authorize to move in positive row
        int magnitude = (kingsCanFly && Cell::isKing(piece)) ? nRows : 1;

        int newPos;
        for (int tr=tr_min; tr<=tr_max; tr+=2){
            for (int tc=-1; tc<=1; tc+=2){
                for (int k=1; k<=magnitude; k++){
                    newPos = RCtoIndex(r + k*tr, c + k*tc);
                    if ( !isValidRC(r + k*tr, c + k*tc) || cells[newPos]!=Cell::empty ) break;
                    possibleMoves.push_back( new CSimpleMove(cellIndex, newPos) );
                }
            }
        }
        return possibleMoves;
    }


    std::vector<CMove*> CBoardState::findPossibleMoves(const bool white){
   //     Find valid moves and their corresponding states for a given player.
   //
   //     Input:
   //         - color: the color of the player we want to find moves
   //     Outputs:
   //         - moves: the list containing very authhorized move.

        std::vector<CMove*> moves;

        // First we look for capturing moves (we are obliged to capture as many pieces as possible)
        std::vector<CCaptureMove*> pieceMoves;
        int maxCaptures = 0;
        int nbCaptures;
        char piece;
        for(int i = 0; i<nCells; ++i){
            piece = cells[i];
            if(piece!=Cell::empty && Cell::isWhite(piece)==white){
                pieceMoves = tryJumpFrom(i);
                if(!pieceMoves.empty()){
                    nbCaptures = pieceMoves[0]->len();
                    if(nbCaptures > maxCaptures){
                        moves.clear();
                        maxCaptures = nbCaptures;
                    }
                    if(nbCaptures >= maxCaptures){
                        moves.insert(moves.end(), pieceMoves.begin(), pieceMoves.end());
                    }
                }
            }
        }

        // If there is no capture move possible, we find simple moves
        if(moves.empty()){
            std::vector<CSimpleMove*> pieceMoves;
            for(int i = 0; i<nCells; ++i){
                piece = cells[i];
                if(piece!=Cell::empty && Cell::isWhite(piece)==white){
                    pieceMoves = tryMoveFrom(i);
                    moves.insert(moves.end(), pieceMoves.begin(), pieceMoves.end());
                }
            }
        }

        return moves;
    }


    void CBoardState::doMove(const CMove& move){
        /* Update the state according to the specified move

        Note that this function does not check if the move is valid*/
        std::list<int> mCells = move.getCells();
        int start = mCells.front();
        if (!isValidIndex(start)) {throw "Invalid Index !";}
        int end = mCells.back();
        char piece = cells[start];
        int diff1,diff2,tr,tc,current_r,current_c;

        if(move.isCapture()){
            std::pair<int,int> RC = indexToRC(start);
            std::pair<int,int> nextRC;
            for (std::list<int>::iterator it = ++mCells.begin(); it != mCells.end(); ++it){
                if (!isValidIndex(*it)) {throw "Invalid Index !";}
                nextRC = indexToRC(*it);

                diff1 = nextRC.first-RC.first;
                diff2 = nextRC.second-RC.second;
                if(!( abs(diff1)==abs(diff2) )) {throw "Invalid Move !";}
                tr = sign(diff1);
                tc = sign(diff2);
                current_r = RC.first + tr;
                current_c = RC.second + tc;
                do{
                    setCell(current_r,current_c, Cell::empty);
                    current_r = current_r + tr;
                    current_c = current_c + tc;
                }while (current_r != nextRC.first);

                RC = nextRC;
            }
        }
        cells[start] = Cell::empty;
        cells[end] = piece;
        std::pair<int,int> endRC = indexToRC(end);

        if( (piece == Cell::w && endRC.first==0)  || (piece == Cell::b && endRC.first==nRows-1) ){
            cells[end] = Cell::promote(piece);
        }
    }

    int CBoardState::sign(const int x){
        if (x==0) return 0;
        return (x>0) ? 1 : -1;
    }

}
