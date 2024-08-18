from chesspiece import Chesspiece

#============================================================================================
#     Square class
#============================================================================================
#each Chessboard needs 64 squares, each sqaure can be empty or have a piece
class Square:
    #constructor, will make the square have no piece, but will indicate it's location on the board using rank and file as x and y
    def __init__(self, pRank, pFile):
        self._ChessPiece = None
        self._rank = pRank
        self._file = pFile

    #getter
    #return: returns true if the square has a chesspiece on it, false if not
    def hasChessPiece(self):
        if isinstance(self._ChessPiece, Chesspiece):
            return True

        return False
    
    #return: returns the chesspiece member variable itself
    def getChessPiece(self):
        return self._ChessPiece
    
    #return the square's rank
    def getRank(self):
        return self._rank
    
    #return the square's file
    def getFile(self):
        return self._file
    
    #return: the location of the piece as a string, using the square object, in file-rank form (A6)
    def getLocation(self):
        letters = ['A','B','C','D','E','F','G','H']

        #add 1 to the rank since cs index'ing starts at 0
        output = "" + letters[7-self.getFile()] + str(self.getRank()+1)

        return output
    
    #setter
    #sets the chesspiece on the square to passed in chess piece in the parameter
    def setChessPiece(self, pChessPiece):
        self._ChessPiece = pChessPiece

    #removes the chess piece on the square and makes the member variable false
    def removeChessPiece(self):
        self._ChessPiece = None