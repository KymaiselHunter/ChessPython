#superclass, general chess piece
#holds the coordinates(rank and file)
#also teams (home will correspond with first player aka white in a normal chess game)
class Chesspiece:
    def __init__(self, pRank, pFile, pHome):
        self._rank = pRank
        self._file = pFile
        if(pHome == True):
            self._home = True
        else:
            self._home = False

        self._pieceType = 'P'

    def getPieceType(self):
        return self._pieceType