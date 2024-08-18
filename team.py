#============================================================================================
#     Team class
#============================================================================================
#a chessboard HAS TWO teams
class Team:
    def __init__(self):
        #list of pieces
        self._pieceList = []

        #variable to keep track if it's in check
        self._check = False

        #rook member variables so we can instanly access castleability when printing it
        self._kingSideRook = None
        self._queenSideRook = None

    #getters
    #return: the list of pieces 
    def getPieceList(self):
        return self._pieceList
    
    #return: the _check member variable that indicates if this team is in check
    def inCheck(self):
        return self._check
    
    #return: the amount of valid squares a team has
    def getAmountOfValidMoves(self):
        count = 0
        for piece in self._pieceList:
            count += piece.getAmountOfValidMoves()

        return count
    
    #return: king side rook
    def getKingSideRook(self):
        return self._kingSideRook
    
    #return: queen side rook
    def getQueenSideRook(self):
        return self._queenSideRook

    #setters
    #post: set the _check variable equal to pCheck
    def setCheck(self, pCheck):
        self._check = pCheck

    #param: piece that will be added to the pieceList
    #post: adds the piece to the list
    def addPieceToTeam(self, pChessPiece):
        self._pieceList.append(pChessPiece)

    #param: piece that will be removed from the pieceList
    #post: removes the piece from the piece lists
    def removePieceFromTeam(self, pChessPiece):
        self._pieceList.remove(pChessPiece)

    #post: set the _kingSideRook
    def setKingSideRook(self, pRook):
        self._kingSideRook = pRook

    #post: set the _queenSideRook
    def setQueenSideRook(self, pRook):
        self._queenSideRook = pRook