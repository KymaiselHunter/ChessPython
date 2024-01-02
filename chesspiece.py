#superclass, general chess piece
#holds the coordinates(rank and file)
#also teams (home will correspond with first player aka white in a normal chess game)
class Chesspiece:
    def __init__(self, pSquare, pHome):
        self._square = pSquare

        if(pHome == True):
            self._home = True
        else:
            self._home = False

        self._pieceType = '!'

    #getters
    def getPieceType(self):
        return self._pieceType
    
    def getPieceAllegiance(self):
        return self._home
    
    #setters
    def removeSquare(self):
        self._square = False

    def setSquare(self, pSquare):
        self._square = pSquare

#============================================= 
#subclasseses of piece(aka the specific types)
#=============================================
            
#first subclass will be the pawns, the heart of chess
class Pawn(Chesspiece):
    def __init__(self, pSquare, pHome):
        super().__init__(pSquare, pHome)
        self._pieceType = 'P'

#King, is also the threshold for winning the game
class King(Chesspiece):
    def __init__(self, pSquare, pHome):
        super().__init__(pSquare, pHome)
        self._pieceType = 'K'

#Queen, most powerful piece, yet most vunerable
class Queen(Chesspiece):
    def __init__(self, pSquare, pHome):
        super().__init__(pSquare, pHome)
        self._pieceType = 'Q'

#Bishop, sniper peice
class Bishop(Chesspiece):
    def __init__(self, pSquare, pHome):
        super().__init__(pSquare, pHome)
        self._pieceType = 'B'

#Knight, funniest peice
class Bishop(Chesspiece):
    def __init__(self, pSquare, pHome):
        super().__init__(pSquare, pHome)
        self._pieceType = 'K'

#Rooks, coolest peice
class Bishop(Chesspiece):
    def __init__(self, pSquare, pHome):
        super().__init__(pSquare, pHome)
        self._pieceType = 'R'      