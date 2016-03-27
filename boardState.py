from .cpp.boardState import BoardState

''' 
Representation of a board state

* Cells are numbered as follows (example for a 8x8 board with 12 pieces):
*
*    col 0  1  2  3  4  5  6  7
* row  -------------------------  row
*  0  |     0     1     2     3 |  0
*  1  |  4     5     6     7    |  1
*  2  |     8     9    10    11 |  2
*  3  | 12    13    14    15    |  3
*  4  |    16    17    18    19 |  4
*  5  | 20    21    22    23    |  5
*  6  |    24    25    26    27 |  6
*  7  | 28    29    30    31    |  7
*      -------------------------
*    col 0  1  2  3  4  5  6  7
*
* The starting board looks like this:
*
*    col 0  1  2  3  4  5  6  7
* row  -------------------------
*  0  |    bb    bb    bb    bb |  
*  1  | bb    bb    bb    bb    |  
*  2  |    bb    bb    bb    bb |  
*  3  | ..    ..    ..    ..    |  
*  4  |    ..    ..    ..    .. |  
*  5  | ww    ww    ww    ww    |  
*  6  |    ww    ww    ww    ww |  
*  7  | ww    ww    ww    ww    |  
*      -------------------------
*        0  1  2  3  4  5  6  7
*
* The black player starts from the top of the board
* The white player starts from the bottom of the board 
'''

