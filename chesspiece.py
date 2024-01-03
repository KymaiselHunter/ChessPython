#superclass, general chess piece
#holds the coordinates(rank and file)
#also teams (home will correspond with first player aka white in a normal chess game)
class Chesspiece:
    def __init__(self, pHome):  
        self._square = False
        
        if(pHome == True):
            self._home = True
        else:
            self._home = False

        self._pieceType = '!'

        #empty vision until it gets a square
        self.clearVision()

    #==============================================
    #getters
    #==============================================
    
    #return: the character that represents the type of piece
    def getPieceType(self):
        return self._pieceType
    
    #return: true if it's white, false if it's black
    def getPieceAllegiance(self):
        return self._home
    
    #return: the square that this chesspiece is currently on
    def getSquare(self):
        return self._square

    def getSquareLocation(self):
        return self._square.getLocation()
    
    #==============================================
    #setters
    #==============================================
    def removeSquare(self):
        self._square = False

    def setSquare(self, pSquare):
        self._square = pSquare

    #vision setters to just exist to be overrided, for now, they should be empty lists
    #clear vision should be helpful to reset the lists when ever moved off the square
    def clearVision(self):
        #removed vision full since it's not needed tbh
        #vision full will be a list of all the squares the piece could see on an empty chessboard
        #self._visionFull = []

        #vision actual will be a list of all square the piece can actually see, ex a bishop cant see past the pawn it's way
        #for a pawn specifically, the pawn can only move to it's left or right if there's an enemy on that square
        self._visionActual = []
    
    #set the visions to nothing since this piece should not have anything as it would abstract in an actual game
    def setVision(self):
        #self._visionFull = [self._square]
        self._visionActual = []

    #return: the list of squares this chess piece sees in it's vision
    def getVision(self):
        return self._visionActual 
    
    #return: a list of strings of the location of the squares in this chess peice's vision
    def getVisionLocations(self):
        return list(map(lambda x: x.getLocation(), self._visionActual))
    
    #param: square that is to be added to the piece's vision
    #post: add a square to the vision
    def addSquareToVision(self, pSquare):
        self._visionActual.append(pSquare)

    #==============================================
    #prints
    #==============================================
    #post: prints the piece's type, color, location and vision
    def printVision(self):
        print("White" if self._home else "Black", type(self), self.getSquareLocation(), self.getVisionLocations(), "\n")

#=========================================================================================================================================
#subclasseses of piece(aka the specific types)
#=========================================================================================================================================
            
#first subclass will be the pawns, the heart of chess
class Pawn(Chesspiece):
    def __init__(self, pHome):
        super().__init__(pHome)
        self._pieceType = 'P'

#King, is also the threshold for winning the game
class King(Chesspiece):
    def __init__(self, pHome):
        super().__init__(pHome)
        self._pieceType = 'K'

#Queen, most powerful piece, yet most vunerable
class Queen(Chesspiece):
    def __init__(self, pHome):
        super().__init__(pHome)
        self._pieceType = 'Q'

#Bishop, sniper peice
class Bishop(Chesspiece):
    def __init__(self, pHome):
        super().__init__(pHome)
        self._pieceType = 'B'

#Knight, funniest peice
class Knight(Chesspiece):
    def __init__(self, pHome):
        super().__init__(pHome)
        self._pieceType = 'N'

#Rooks, coolest peice
class Rook(Chesspiece):
    def __init__(self, pHome):
        super().__init__(pHome)
        self._pieceType = 'R'      