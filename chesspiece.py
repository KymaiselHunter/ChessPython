#superclass, general chess piece
#holds the coordinates(rank and file)
#also teams (home will correspond with first player aka white in a normal chess game)
class Chesspiece:
    def __init__(self, pHome):  
        self._square = None
        
        if(pHome == True):
            self._home = True
        else:
            self._home = False

        self._pieceType = '!'

        #empty vision until it gets a square
        self.clearVision()

        #member variable int to see how many moves were made, good for pawn double jump
        self._moveCount = 0

        #empty valid moves until it's on a square and the vision in calculate
        self.clearValidMoves()

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
    
    #
    def hasSquare(self):
        if self._square:
            return True
        
        return False

    ##return: the location of the piece as a string, using the square object, in file-rank form (A6)(calls the func in square class)
    def getSquareLocation(self):
        return self._square.getLocation()
    
    #return: the moveCounter variable
    def getMoveCount(self):
        return self._moveCount
    
    #==============================================
    #setters
    #==============================================
    def removeSquare(self):
        self._square = False

    def setSquare(self, pSquare):
        self._square = pSquare

    def increaseMoveCount(self):
        self._moveCount += 1

    #==============================================
    #vision setters and getters
    #==============================================

    #vision setters to just exist to be overrided, for now, they should be empty lists
    #clear vision should be helpful to reset the lists when ever moved off the square
    def clearVision(self):
        #removed vision full since it's not needed tbh
        #vision full will be a list of all the squares the piece could see on an empty chessboard
        #self._visionFull = []

        #vision actual will be a list of all square the piece can actually see, ex a bishop cant see past the pawn it's way
        #for a pawn specifically, the pawn can only move to it's left or right if there's an enemy on that square
        self._vision = []
    
    #set the visions to nothing since this piece should not have anything as it would abstract in an actual game
    def setVision(self):
        #self._visionFull = [self._square]
        self._vision = []

    #return: the list of squares this chess piece sees in it's vision
    def getVision(self):
        return self._vision 
    
    #param: square that is to be added to the piece's vision
    #post: add a square to the vision
    def addSquareToVision(self, pSquare):
        self._vision.append(pSquare)

    #==============================================
    #valid moves setters and getters
    #==============================================
    #using the vision, the chessboard can then calculate what squares are valid moves
    
    #post: clears the current Valid moves
    def clearValidMoves(self):
        self._validMoves = []

    #return: the amount of valid moves this piece has
    def getAmountOfValidMoves(self):
        return len(self._validMoves)
    
    #param: square that is to be added to the piece's validMoveList
    #post: add a square to the validMoves
    def addSquareToValidMoves(self, pSquare):
        self._validMoves.append(pSquare)

    #return: the list of valid moves this chess piece can make
    def getValidMoves(self):
        return self._validMoves

    #==============================================
    #prints
    #==============================================
    #post: prints the piece's type, color, location and vision
    def printVision(self):
        print("White" if self._home else "Black", type(self), self.getSquareLocation(), self.getVisionLocations(), "\n")

    #return: a list of strings of the location of the squares in this chess peice's vision
    def getVisionLocations(self):
        return list(map(lambda x: x.getLocation(), self._vision))
    
    #post: prints the pieces' type, color, location and possible moves
    def printValidMoves(self):
        print("White" if self._home else "Black", type(self), self.getSquareLocation(), self.getValidMovesLocations(), "\n")

    #return: a list of strings of the location of the squares of this chess piece's possible moves
    def getValidMovesLocations(self):
        return list(map(lambda x: x.getLocation(), self._validMoves))

#=========================================================================================================================================
#subclasseses of piece(aka the specific types)
#=========================================================================================================================================
            
#first subclass will be the pawns, the heart of chess
class Pawn(Chesspiece):
    def __init__(self, pHome):
        super().__init__(pHome)
        self._pieceType = 'P'
        self._nextSquare = None
        self._jumpSquare = None
        self._jumpTime = None

    #pawn needs these as it's movement + vision is strange, only being able to move to vision squares if it can take
    #only able to move forward if the next square is empty

    #return next square member variable
    def getNextSquare(self):
        return self._nextSquare
    
    #param: reference to the square will move in front to
    def setNextSquare(self, pSquare):
        self._nextSquare = pSquare

    #return jump square member variable
    def getJumpSquare(self):
        return self._jumpSquare
    
    #param: reference to the square that the piece can jump to
    def setJumpSquare(self, pSquare):
        self._jumpSquare = pSquare

    #return jump time member variable
    def getJumpTime(self):
        return self._jumpTime
    
    #param: int representing the time(length of history) t
    def setJumpTime(self, pTime):
        self._jumpTime = pTime

    #==============================================
    #prints(override this for pawn due to needing the front squares as well)
    #==============================================
    #post: prints the piece's type, color, location and vision
    def printVision(self):
        print("White" if self._home else "Black", type(self), self.getSquareLocation(), self.getVisionLocations(), 
            [self._nextSquare.getLocation() if self._nextSquare else "No front", 
             self._jumpSquare.getLocation() if self._jumpSquare else "No Jump"],"\n")

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

        #extra member variables since rooks can castle
        #we need a member variable to hold the square this rook will go to
        #we need a member variable to hold the square the king will go
        #we need a member variable list to hold all the squares that need to be clear in order to castle

        self._rookDestination = None
        self._kingDestination = None
        self._castleSquares = []

        #because i didnt really plan well enough for the casteling part of this, i decided to
        #make a pointer to the king in the rook subclass so we dont have to loop 
        #everytime to check for the king being in check or not
        self._kingPointer = None

    #setters and getters for the special rook member variables
    #return: rookDestination
    def getRookDestination(self):
        return self._rookDestination
    
    #param: square that the rook should land on
    #post: saves the square the rook should land on in the rookDestination member variable
    def setRookDestination(self, pSquare):
        self._rookDestination = pSquare

    #return: kingDestination
    def getKingDestination(self):
        return self._kingDestination
    
    #param: square that the king should land on
    #post: saves the square the king should land on in the rookDestination member variable
    def setKingDestination(self, pSquare):
        self._kingDestination = pSquare
    
    #return the list of squares that should be clear to get this rook to castle
    def getCastleSquares(self):
        return self._castleSquares
    
    #param: square that needs to be cleared inorder to castle
    def addCastleSquare(self, pSquare):
        self._castleSquares.append(pSquare)

    #return: kingPointer
    def getKing(self):
        return self._kingPointer
    
    #param: king of the team this rook is on
    #post: saves the king so that the rook can access it's stuff in O(1) time
    def setKing(self, pKing):
        self._kingPointer = pKing
