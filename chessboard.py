from chesspiece import Chesspiece

#each Chessboard needs 64 squares, each sqaure can be empty or have a piece

class Square:
    #member variable to hold either the piece or boolean saying there is no piece
    def __init__(self):
        self._ChessPiece = False

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
        


class Chessboard:
    #create an empty chessboard(matrix of 8x8 empty sqaures )
    def __init__(self):
        self._matrix = [[Square() for i in range(8) ]  for j in range(8)]

    def displayBoard(self):
        print("==================")
        for row in self._matrix:
            displayString = "|"

            for sq in row:
                if(sq.hasChessPiece() == False):
                    displayString = displayString + " |"
                else:
                    displayString = displayString + sq.getChessPiece().getPieceType() + "|"
            
            print(displayString)

        print("==================")

    def testSet(self):
        self._matrix[5][2].setChessPiece(Chesspiece(5,2, True))

            
            