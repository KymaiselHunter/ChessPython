from chesspiece import Chesspiece

#each Chessboard needs 64 squares, each sqaure can be empty or have a piece

class Square:
    #member variable to hold either the piece or boolean saying there is no piece
    def __init__(self, pRank, pFile):
        self._ChessPiece = False
        self._rank = pRank
        self._file = pFile

    #getter
    def hasChessPiece(self):
        if(type(self._ChessPiece) is bool):
            return False

        return True
    
    def getChessPiece(self):
        return self._ChessPiece
    
    #setter
    def setChessPiece(self, pChessPiece):
        self._ChessPiece = pChessPiece

    def removeChessPiece(self):
        self._ChessPiece = False
        


class Chessboard:
    #create an empty chessboard(matrix of 8x8 empty sqaures )
    def __init__(self):
        #matrix of the board itself
        self._matrix = [[Square(j,i) for i in range(8) ]  for j in range(8)]

        #boolean to keep track of whose turn
        self._homeTurn = True

        #list of pieces for each team
        self._homePieces = []
        self._vistorPieces = []

    def displayBoard(self):
        print("==========================")
        for row in self._matrix:
            displayString = "|"

            for sq in row:
                if(sq.hasChessPiece() == False):
                    displayString = displayString + "  |"
                else:
                    if(sq.getChessPiece().getPieceAllegiance()):
                        displayString = displayString + 'W' 
                    else: 
                        displayString = displayString + 'B'
                    displayString = displayString + sq.getChessPiece().getPieceType() + "|"
            
            print(displayString)

        print("==========================")

    #param: the square that the piece will be removed from
    #post: if the sqaure has no piece return false, if it does have a piece, remove it from the matrix, 
    #team and remove the square from the piece then return true
    def removePieceFromChessBoard(self, pSquare):
        if(not pSquare.hasChessPiece()):
            return False
        if(pSquare.getChessPiece().getPieceAllegiance()):
            self._homePieces.remove(pSquare.getChessPiece())
        else:
            self._vistorPieces.remove(pSquare.getChessPiece())

        pSquare.getChessPiece().removeSquare()
        pSquare.removeChessPiece()

    #post: calls the removePieceFromChessBoard on all squares in the matrix
    def clearBoard(self):
        for rank in self._matrix:
            for square in rank:
                self.removePieceFromChessBoard(square)

    #param: pNewPiece - the piece to be added to the baord
    #param: pSquare - the square the piece will be added to 
    #post: adds a piece to the board, meaning, to the matrix, teams and it's square
    #returns true if added correctly, returns false if there is already a piece on the square
    def addPieceToChessBoard(self, pNewPiece, pSquare):
        #early exit if failure to add to board
        if(pSquare.hasChessPiece()):
            return False
        
        if(pNewPiece.getPieceAllegiance()):
            self._homePieces.append(pNewPiece)
        else:
            self._vistorPieces.append(pNewPiece)
        
        pSquare.setChessPiece(pNewPiece)
        pNewPiece.setSquare(pSquare)

        return True

        


            
            