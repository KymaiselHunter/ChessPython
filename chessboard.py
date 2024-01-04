from chesspiece import Chesspiece
from chesspiece import Pawn
from chesspiece import Rook
from chesspiece import Knight
from chesspiece import Bishop
from chesspiece import Queen
from chesspiece import King

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

    def printBoard(self):
        print("==========================")
        for row in self._matrix:
            displayString = "|"

            for sq in row:
                if sq.hasChessPiece():
                    if(sq.getChessPiece().getPieceAllegiance()):
                        displayString = displayString + 'W' 
                    else: 
                        displayString = displayString + 'B'
                    displayString = displayString + sq.getChessPiece().getPieceType() + "|"
                else:
                    displayString = displayString + "  |"
            
            print(displayString)

        print("==========================")

    #==============================================
    #     Handeling adding and removing pieces
    #==============================================
        
    #param: the square that the piece will be removed from
    #post: if the sqaure has no piece return false, if it does have a piece, remove it from the matrix, 
    #team and remove the square from the piece then return true
    def removePieceFromChessBoard(self, pSquare):
        if not pSquare.hasChessPiece():
            return False
        
        if(pSquare.getChessPiece().getPieceAllegiance()):
            self._homePieces.remove(pSquare.getChessPiece())
        else:
            self._vistorPieces.remove(pSquare.getChessPiece())

        pSquare.getChessPiece().removeSquare()
        pSquare.removeChessPiece()

        #every addition and removal affects all visions
        self.updateVisionAll()

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

        #every addition and removal affects all visions
        self.updateVisionAll()

        return True
    
    #==============================================
    # Handeling vision updates to the pieces
    #==============================================
    
    #post: will update the visions of all of the pieces 
    def updateVisionAll(self):
        #update white/home
        self.updateVisionTeam(True)
        
        #update black/visitor
        self.updateVisionTeam(False)
    
    #param: home team or vistor team will have their visions updated    
    #post: loop through the pieces on that team, and update each one
    def updateVisionTeam(self, pHome):
        if pHome:
            for piece in self._homePieces:
                self.updateVisionPiece(piece)
        else:
            for piece in self._vistorPieces:
                self.updateVisionPiece(piece)


    #param: the piece that will be updated
    #post: update the vision of that single piece
    #return: true/false if the update is successful
    def updateVisionPiece(self, pChessPiece):
        #first clear the previous vision of the piece
        pChessPiece.clearVision()
        
        #quick exit incase the chessPiece in the param is not a piece or the chess piece isnt on a square
        if not isinstance(pChessPiece, Chesspiece) or not pChessPiece.hasSquare():
            return False
        
        #now update based on piece type, return true after all ifs, if it hits the else of none of the subclass pieces, early return false
        if isinstance(pChessPiece, Rook):
            self.updateVisionRook(pChessPiece)
        elif isinstance(pChessPiece, Bishop):
            self.updateVisionBishop(pChessPiece)
        elif isinstance(pChessPiece, Queen):
            #queen's movement is just rook and bishop combined
            self.updateVisionRook(pChessPiece)
            self.updateVisionBishop(pChessPiece)
        elif isinstance(pChessPiece, King):
            self.updateVisionKing(pChessPiece)
        elif isinstance(pChessPiece, Knight):
            self.updateVisionKnight(pChessPiece)
        elif isinstance(pChessPiece, Pawn):
            self.updateVisionPawn(pChessPiece)
        else: 
            #return false if it's not a valid piece
            return False

        
        return True


    #param: the ROOK that will be updated
    #post: update the vision for specifically ROOKS
    def updateVisionRook(self, pRook):
        #get the square the piece is on
        currentSquare = pRook.getSquare()
        
        #nested for loop, first will check if it should affect the rank or the file
        for plane in ["Rank", "File"]:
            for iterator in [-1, 1]:
                #boolean that will represent if the vision is being blocked
                block = False

                currRank = currentSquare.getRank()
                currFile = currentSquare.getFile()

                #itearate first so it doesnt include it's own square
                if plane == "Rank":
                    currRank += iterator
                else:
                    currFile += iterator

                while self.inBounds(currRank, currFile) and not block:
                    visionSquare = self._matrix[currRank][currFile]
                    #print("Rook on", pRook.getSquareLocation(), visionSquare.getLocation(), visionSquare.hasChessPiece())
                    if visionSquare.hasChessPiece():
                        block = True

                    pRook.addSquareToVision(visionSquare)
                    if plane == "Rank":
                        currRank += iterator
                    else:
                        currFile += iterator

    #param: the BISHOP that will be updated
    #post: update the vision for specifically BISHOPs
    def updateVisionBishop(self, pBishop):
        #get the square the piece is on
        currentSquare = pBishop.getSquare()
        
        #nested for loop, first will check if it should affect the rank or the file
        for x in [-1, 1]:
            for y in [-1, 1]:
                #boolean that will represent if the vision is being blocked
                block = False

                currRank = currentSquare.getRank()
                currFile = currentSquare.getFile()

                #itearate first so it doesnt include it's own square
                #for bishops, add both from x and y due to it being diagnol
                currRank += x
                currFile += y

                while self.inBounds(currRank, currFile) and not block:
                    visionSquare = self._matrix[currRank][currFile]
                    #print("Bishop on", pBishop.getSquareLocation(), visionSquare.getLocation(), visionSquare.hasChessPiece())
                    if visionSquare.hasChessPiece():
                        block = True

                    pBishop.addSquareToVision(visionSquare)
                    currRank += x
                    currFile += y

    #param: the KING that will be updated
    #post: update the vision for specifically KINGS
    def updateVisionKing(self, pKing):
        #get the square the piece is on
        currentSquare = pKing.getSquare()
        
        #nested for loop, first will check if it should affect the rank or the file
        for x in [-1, 0, 1]:
            for y in [-1,0, 1]:
                #skip iteration if ur checking the currSquare
                if x == 0 and y == 0:
                    continue

                currRank = currentSquare.getRank() + x
                currFile = currentSquare.getFile() + y

                #check once, no while loop since the king can only move 1 square

                if self.inBounds(currRank, currFile):
                    visionSquare = self._matrix[currRank][currFile]
                    #print("Bishop on", pBishop.getSquareLocation(), visionSquare.getLocation(), visionSquare.hasChessPiece())

                    pKing.addSquareToVision(visionSquare)


    #param: the KNIGHT that will be updated
    #post: update the vision for specifically the KNIGHTS
    def updateVisionKnight(self, pKnight):
        #get the square the piece is on 
        currentSquare = pKnight.getSquare()

        #for loop, goes through 4 things, simulates 4 quadrants of a plane with the knight being the origin
        for quadrants in [[1,1], [1,-1], [-1,1], [-1,-1]]:
            firstRank = currentSquare.getRank() + 2 * quadrants[0]
            firstFile = currentSquare.getFile() + 1 * quadrants[1] 

            secondRank = currentSquare.getRank() + 1 * quadrants[0]
            secondFile = currentSquare.getFile() + 2 * quadrants[1]

            if self.inBounds(firstRank, firstFile): 
                pKnight.addSquareToVision(self._matrix[firstRank][firstFile])

            if self.inBounds(secondRank, secondFile): 
                pKnight.addSquareToVision(self._matrix[secondRank][secondFile])

    #param: the PAWN that will be updated
    #post: update the viosion for specically the PAWNS
    def updateVisionPawn(self, pPawn):
        #get the square the piece is on 
        currentSquare = pPawn.getSquare()
        
        direction = 0

        #if it's white, it should increase the rank, else, decrease
        if pPawn.getPieceAllegiance():
            direction = 1
        else: 
            direction = -1

        #no for loop since pawns are even more strange than the king,
        #will also have to check movement square seperately from it's vision squares
            
        currRank = currentSquare.getRank() + direction 
        currFile = currentSquare.getFile() 
        
        #first we will do the front square since i feel as if that's the easiest
        if self.inBounds(currRank, currFile):
            nextSquare = self._matrix[currRank][currFile]
            pPawn.setNextSquare(nextSquare)
            
            #if the square infront of it has not piece and the pawn hasnt moved, it can see it's jumpable square and it's inBounds
            if pPawn.getMoveCount() == 0 and not nextSquare.hasChessPiece() and self.inBounds(currRank+direction, currFile):
                pPawn.setJumpSquare(self._matrix[currRank + direction][currFile])
                print(pPawn.getMoveCount() == 0 and not nextSquare.hasChessPiece() and self.inBounds(currRank+direction, currFile))


        #now we do it's vision
        if self.inBounds(currRank, currFile - 1):
            pPawn.addSquareToVision(self._matrix[currRank][currFile-1])

        if self.inBounds(currRank, currFile + 1):
            pPawn.addSquareToVision(self._matrix[currRank][currFile + 1]) 



    #print all the visions of a team, will most likely be used for testing rn, but maybe modify to show all danger squares for king
    #param: home team or vistor team will have their visions printed   
    #post: loop through the pieces on that team, and print each one along with their visions
    def printTeamVision(self, pHome):
        team = None
        if pHome:
            team = self._homePieces
            print("White Pieces")
        else:
            team = self._vistorPieces
            print("Black Pieces")

        for piece in team:
            piece.printVision()
        
        print("-End-")

    #[REMOVED AND PUT INTO CHESS PIECE CLASS]
    #param: piece that will be printed with it's vision
    #post: prints the vision of a specific piece
    #def printPieceVision(self, pChessPiece):
    #    print(type(pChessPiece), pChessPiece.getSquareLocation(), pChessPiece.getVisionLocations(), "\n")

    #helper for getting visions
    #param: rank
    #param: file
    #return: true if the rank and file are numbers contained on the board
    def inBounds(self, pRank, pFile):
        if pRank < 0 or pRank >= 8:
            return False
        
        if pFile < 0 or pFile >= 8:
            return False

        return True

    #==============================================
    # Handeling Board setup
    #==============================================
    
    #param: row that will be filled with pawns
    #param: color that the pieces should be
    #post: fills that rank with pawns of pHome allegience
    def placeRankOfPawns(self, pRank, pHome):
        #for loop for pawns
        for square in self._matrix[pRank]:
            self.addPieceToChessBoard(Pawn(pHome), square)

    #param: row that will be filled with the default backrank setup
    #param: color that the pieces should be
    def placeDefaultBackRank(self, pRank, pHome):
        #manually for each thingy
        #rooks
        self.addPieceToChessBoard(Rook(pHome), self._matrix[pRank][0])
        self.addPieceToChessBoard(Rook(pHome), self._matrix[pRank][-1])

        #knights
        self.addPieceToChessBoard(Knight(pHome), self._matrix[pRank][1])
        self.addPieceToChessBoard(Knight(pHome), self._matrix[pRank][-2])

        #bishops
        self.addPieceToChessBoard(Bishop(pHome), self._matrix[pRank][2])
        self.addPieceToChessBoard(Bishop(pHome), self._matrix[pRank][-3])

        #royalty, king and queen
        self.addPieceToChessBoard(King(pHome), self._matrix[pRank][3])
        self.addPieceToChessBoard(Queen(pHome), self._matrix[pRank][-4])
        

    #post: cleans the board and sets up the board for a new default game
    def setUpChessBoard(self):
        #removes all pieces from the board and teams
        self.clearBoard()

        #reset the turn to white/home
        self._homeTurn = True
        
        #lets do the black/visitor team first
        #black pawn row
        self.placeRankOfPawns(6, False)

        #black backrank
        self.placeDefaultBackRank(7, False)

        #now for the white/home team
        #white pawn row
        self.placeRankOfPawns(1, True)

        #white backrank
        self.placeDefaultBackRank(0,True)           
            