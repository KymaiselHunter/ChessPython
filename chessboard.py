from chesspiece import Chesspiece
from chesspiece import Pawn
from chesspiece import Rook
from chesspiece import Knight
from chesspiece import Bishop
from chesspiece import Queen
from chesspiece import King

#copy will be used for a version control of the board itself
import copy

#pygame imports
import sys

import pygame


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



#============================================================================================
#     Chessboard class
#============================================================================================
class Chessboard:
    #create an empty chessboard(matrix of 8x8 empty sqaures )
    def __init__(self, *args):
        if len(args) == 0: 
            #matrix of the board itself
            self._matrix = [[Square(j,i) for i in range(8) ]  for j in range(8)]

            #boolean to keep track of whose turn
            self._homeTurn = True

            #list of pieces for each team
            self._homeTeam = Team()
            self._vistorTeam = Team()

            #member variable that acts as a queue for version control
            #the board history, when adding a list into it, it should contain 4 things
            #  0        1           2           3
            # matrix    homeTurn     HomeTeam    visitor team
            self._boardHistory = []

            #handling drawing
            pygame.init()

            pygame.display.set_caption("Kyle's Chess in Python")
            self._screen = pygame.display.set_mode((1000, 800))
            self._clock = pygame.time.Clock()

        else:
            #if the parameters is a list with 4 elements, means that it's being used to calculate future moves
            #so all of the member variables will have values in the param constructor
            #bri'ish pythons be like, that's a constructor, init
            self._matrix = args[0][0]
            self._homeTurn = args[0][1]
            self._homeTeam = args[0][2]
            self._vistorTeam = args[0][3]

            self._boardHistory = []

        #constants
        #black board constants
        self._BLACK_BOARD_LENGTH = 755
        self._BLACK_BOARD_COORDINATES = (0, 10)
        #image dictionaries
        self._NEUTRAL_IMAGE_URL = {
            "Board" : pygame.image.load('assets/images/chessboardCom.png')
        }
        #self._NEUTRAL_IMAGE_URL['Board'] = pygame.transform.scale(self._NEUTRAL_IMAGE_URL['Board'], (pLength, pLength))

        self._PIECE_IMAGE_URL_RED = {
            "Pawn" : pygame.image.load('assets/images/pawnRed.png'),
            "Rook" : pygame.image.load('assets/images/rookRed.png')
        }

        self._PIECE_IMAGE_URL_PURPLE = {
            "Pawn" : pygame.image.load('assets/images/pawnPurple.png'),
            "Rook" : pygame.image.load('assets/images/rookPurple.png')
        }

        

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
            self._homeTeam.removePieceFromTeam(pSquare.getChessPiece())
        else:
            self._vistorTeam.removePieceFromTeam(pSquare.getChessPiece())

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
            self._homeTeam.addPieceToTeam(pNewPiece)
        else:
            self._vistorTeam.addPieceToTeam(pNewPiece)
        
        pSquare.setChessPiece(pNewPiece)
        pNewPiece.setSquare(pSquare)

        #every addition and removal affects all visions
        self.updateVisionAll()

        return True
    
    #============================================================================================
    # Handeling vision updates to the pieces
    #============================================================================================
    
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
            for piece in self._homeTeam.getPieceList():
                self.updateVisionPiece(piece)
        else:
            for piece in self._vistorTeam.getPieceList():
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
                #print(pPawn.getMoveCount() == 0 and not nextSquare.hasChessPiece() and self.inBounds(currRank+direction, currFile))


        #now we do it's vision
        if self.inBounds(currRank, currFile - 1):
            pPawn.addSquareToVision(self._matrix[currRank][currFile-1])

        if self.inBounds(currRank, currFile + 1):
            pPawn.addSquareToVision(self._matrix[currRank][currFile + 1]) 


    

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

    #============================================================================================
    # Handeling Board setup
    #============================================================================================
    
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
        #need to hold rooks as we will add the other pieces to their member variabels
        castleKing = Rook(pHome)
        castleQueen = Rook(pHome)

        if(pHome):
            self._homeTeam.setKingSideRook(castleKing)
            self._homeTeam.setQueenSideRook(castleQueen)
        else:
            self._vistorTeam.setKingSideRook(castleKing)
            self._vistorTeam.setQueenSideRook(castleQueen)
        
        self.addPieceToChessBoard(castleKing, self._matrix[pRank][0])
        self.addPieceToChessBoard(castleQueen, self._matrix[pRank][-1])

        #knights
        self.addPieceToChessBoard(Knight(pHome), self._matrix[pRank][1])
        self.addPieceToChessBoard(Knight(pHome), self._matrix[pRank][-2])

        #bishops
        self.addPieceToChessBoard(Bishop(pHome), self._matrix[pRank][2])
        self.addPieceToChessBoard(Bishop(pHome), self._matrix[pRank][-3])

        #royalty, king and queen
        self.addPieceToChessBoard(King(pHome), self._matrix[pRank][3])
        self.addPieceToChessBoard(Queen(pHome), self._matrix[pRank][-4])

        #set up destination squares for rooks and castle squares
        castleKing.addCastleSquare(self._matrix[pRank][1])
        castleKing.addCastleSquare(self._matrix[pRank][2])

        castleKing.setKingDestination(self._matrix[pRank][1])
        castleKing.setRookDestination(self._matrix[pRank][2])

        castleKing.setKing(self._matrix[pRank][3].getChessPiece())

        castleQueen.addCastleSquare(self._matrix[pRank][-2])
        castleQueen.addCastleSquare(self._matrix[pRank][-3])
        castleQueen.addCastleSquare(self._matrix[pRank][-4])

        castleQueen.setKingDestination(self._matrix[pRank][-3])
        castleQueen.setRookDestination(self._matrix[pRank][-4])

        castleQueen.setKing(self._matrix[pRank][3].getChessPiece())
        

    #post: cleans the board and sets up the board for a new default game
    def setUpChessBoard(self):
        #reset the history
        self.resetHistory()

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

        #now that the board is setup and at the start, start the history
        self.addToHistory()

    #============================================================================================
    # Test Functions (Remove Later)
    #============================================================================================

    #test function to purely test other functions by changing the board
    def testFunc(self):
        self.removePieceFromChessBoard(self._matrix[1][3])
        self.addPieceToChessBoard(Queen(False), self._matrix[5][3])

    #test function to purely test other functions by changing the board
    def testFunc2(self):
        #self.removePieceFromChessBoard(self._matrix[1][3])
        self.addPieceToChessBoard(Knight(False), self._matrix[2][2])

    def testFunc3(self):
        self.removePieceFromChessBoard(self._matrix[1][2])
        self.addPieceToChessBoard(Queen(False), self._matrix[3][0])
        self.addPieceToChessBoard(Knight(True), self._matrix[5][2])
            
    #============================================================================================
    # Prints
    #============================================================================================

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

    #[REMOVED AND PUT INTO CHESS PIECE CLASS]
    #param: piece that will be printed with it's vision
    #post: prints the vision of a specific piece
    #def printPieceVision(self, pChessPiece):
    #    print(type(pChessPiece), pChessPiece.getSquareLocation(), pChessPiece.getVisionLocations(), "\n")

    #print all the visions of a team, will most likely be used for testing rn, but maybe modify to show all danger squares for king
    #param: home team or vistor team will have their visions printed   
    #post: loop through the pieces on that team, and print each one along with their visions
    def printTeamVision(self, pHome):
        team = None
        if pHome:
            team = self._homeTeam
            print("White Pieces Vision")
        else:
            team = self._vistorTeam
            print("Black Pieces Vision")

        for piece in team.getPieceList():
            piece.printVision()
        
        print("-End of Vision-")

    #print all the possible moves of a team, will be used for testing and possible player inputs
    #param: home team or vistor team will have their moves printed   
    #post: loop through the pieces on that team, and print each one along with their moves
    def printTeamValidMoves(self, pHome):
        team = None
        if pHome:
            team = self._homeTeam
            print("White Pieces Valid Moves")
        else:
            team = self._vistorTeam
            print("Black Pieces Valid Moves")

        for piece in team.getPieceList():
            piece.printValidMoves()

        if team.getKingSideRook() and self.canCastle(team.getKingSideRook()):
            print("King Side Castle is Available")
        else:
            print("King Side Castle is not Available")

        if team.getQueenSideRook() and self.canCastle(team.getQueenSideRook()):
            print("Queen Side Castle is Available")
        else: 
            print("Queen Side Castle is not Available")
        
        print("-End of Valid Moves-")

    #============================================================================================
    # Handeling Checks
    #============================================================================================
    #this gonna be using the vision from the previous things to see if in check
    #param: boolean that represents which team i will be checking 
    #if it's true, check if the whiteTeam is in check(loop through black vision), else check the black team(loop through white)
    #return: true if the team is in check, false if the team is not in check
    def isTeamInCheck(self, pHome):
        attackers = None
        defenders = None

        #depending on the parameters, set which one will be the one that needs to loop through their visions,
        #vs which one i need to find the king square [attacker = vision][defender = king]
        if pHome:
            attackers = self._vistorTeam
            defenders = self._homeTeam
        else: 
            attackers = self._homeTeam
            defenders = self._vistorTeam

        #we just need the piece list for this part really
        attackers = attackers.getPieceList()
        defenders = defenders.getPieceList()

        defendersSquare = None

        for piece in defenders:
            if isinstance(piece, King):
                defendersSquare = piece.getSquare()
                break

        #short exit, cant be in check in no king exists
        if defendersSquare == None:
            return False
        
        #now that we have the square the king is on, lets see if this square is in any of the piece vision
        for piece in attackers:
            #if the defender square is found in a piece's vision, return true
            if defendersSquare in piece.getVision():
                return True
        
        #if it isnt found within that loop, the king is not in check, so return false
        return False
    
    #in hindsight i should have made the code in the function more general so i can reuse it 
    #for features such as casteling, but i didnt, hence i will copy and paste some of my own code
    #and use it for handeling castle-ability
    #param: rook on the side that will caslte
    #return: will return ture of false if the rook can castle on that side
    def canCastle(self, pRook):
        #firstly, if the king on the rook's team is currently in check, it cannot castle so early return false
        #this also checks if a king exists
        if(self.isTeamInCheck(pRook.getPieceAllegiance())):
            return False
        
        #secondly, if either the king or rook has moved, also early exit
        if pRook.getMoveCount() > 0 or pRook.getKing().getMoveCount() > 0:
            return False
        
        #not a rule of chess but how the board is setup
        #if there is no castle squares nor destinations, then there will never be any casteling
        if not pRook.getKingDestination() or not pRook.getRookDestination() or len(pRook.getCastleSquares()) == 0:
            return False
        
        #if the squares between the king and rook are not vacant it cannot castle
        for square in pRook.getCastleSquares():
            if square.hasChessPiece():
                return False

        #get the team that is attacking so we can loop through it's vision
        attackers = None

        #depending on the rook alliegience from parameters,
        #set which team will be the one that needs to loop through their visions,
        #vs which one i need to find the castle squares
        if pRook.getPieceAllegiance():
            attackers = self._vistorTeam.getPieceList()
        else: 
            attackers = self._homeTeam.getPieceList()

        #check if the castle squares are in the vision, if one is, then return false
        for piece in attackers:
            #if the destination squares are found in a piece's vision, return False 
            #as squares the king is crossing over or finishing on should not be in check
            if pRook.getKingDestination() in piece.getVision() or pRook.getRookDestination() in piece.getVision():
                return False
            
        #if it gets through, allllll of this, it can castle, so return True
        return True

    #============================================================================================
    # Handeling Version Control
    #============================================================================================
    #since we can now handle checks, i want to create a function that calculates and updates all the possible moves each piece
    #on a team has, that being said, how i want it to work, is that it attempts every move, 
    #after u move, if ur in check; moved ontop of ur own guy; etc, then it's not valid
    #then it should go back to the previous matrix
    #that being said, i need a version control membervariable and functions, then once i have that, i can create the valid moves func
    #once i have that, all i would have left is ending the game, castleing, then the interface of the game
    
    #post: erases the board history and resets the version control variable
    def resetHistory(self):
        self._boardHistory = []

    #will add a list to the history stack, that list will contain copies of the current values inside
    #  0        1           2           3
    # matrix    homeTurn     HomeTeam    visitor team
    def addToHistory(self):
        #make a list of the current values of this 
        newHistory = [self._matrix, self._homeTurn, self._homeTeam, self._vistorTeam]

        #make a deep copy of all of these, i put it in the list first as im hoping the deepcopy will preserve 
        #the links between the chesspieces, and hope the chesspieces in the matrix are the same as the ones in the teams
        newHistory = copy.deepcopy(newHistory)
        self._boardHistory.append(newHistory)

    #============================================================================================
    # Handeling move validation
    #============================================================================================
        
    #
    #param: home team or vistor team will have their valid moves updated    
    #post: loop through the pieces on that team, and update each one
    def updateValidMovesTeam(self, pHome):
        if pHome:
            for piece in self._homeTeam.getPieceList():
                self.updateValidMovesPiece(piece)
        else:
            for piece in self._vistorTeam.getPieceList():
                self.updateValidMovesPiece(piece)

    
    #param: the piece that will be updated
    #post: update the valid moves of that single piece
    #return: true/false if the update is successful
    def updateValidMovesPiece(self, pChessPiece):
        #first clear the previous vision of the piece
        pChessPiece.clearValidMoves()
        
        #quick exit incase the chessPiece in the param is not a piece or the chess piece isnt on a square
        if not isinstance(pChessPiece, Chesspiece) or not pChessPiece.hasSquare():
            return False
        
        #only the pawn has special needs, so if it's a pawn, take care of it differently, but everything else can use the same validation
        if isinstance(pChessPiece, Pawn):
            #lets check the squares u can attack first since that will be similar to the for loop in the other one
            for visionSquare in pChessPiece.getVision():
                #quick skip to next iteration if the square in it's vision has an friendly piece or none at all
                if not visionSquare.hasChessPiece() or visionSquare.getChessPiece().getPieceAllegiance() == pChessPiece.getPieceAllegiance():
                    continue

                futureBoard = Chessboard(copy.deepcopy(self._boardHistory[-1]))
                if futureBoard.validatePossibleMove(pChessPiece.getSquare(), visionSquare):
                    pChessPiece.addSquareToValidMoves(visionSquare)

            #now lets check the none attacking sqaures and just the push forward ones
            #if the chesspiece has a square in front of it and there is no piece there, then we may validate
            nextSquare = pChessPiece.getNextSquare()
            jumpSquare = pChessPiece.getJumpSquare()

            #quick exits cuz without them, the nesting gets disgusting
            if not nextSquare or nextSquare.hasChessPiece():
                return

            futureBoard = Chessboard(copy.deepcopy(self._boardHistory[-1]))
            if not futureBoard.validatePossibleMove(pChessPiece.getSquare(), nextSquare):
                return

            pChessPiece.addSquareToValidMoves(nextSquare)    

            #now for the jump square
            if pChessPiece.getMoveCount() > 0 or not jumpSquare or jumpSquare.hasChessPiece():
                return    

            if futureBoard.validatePossibleMove(nextSquare, jumpSquare):
                pChessPiece.addSquareToValidMoves(jumpSquare)    
        else:
            for visionSquare in pChessPiece.getVision():
                #quick skip to next iteration if the square in it's vision has an friendly piece
                if visionSquare.hasChessPiece() and visionSquare.getChessPiece().getPieceAllegiance() == pChessPiece.getPieceAllegiance():
                    continue

                futureBoard = Chessboard(copy.deepcopy(self._boardHistory[-1]))
                if futureBoard.validatePossibleMove(pChessPiece.getSquare(), visionSquare):
                    pChessPiece.addSquareToValidMoves(visionSquare)
                

        return True



    """
    #DO NOT USE FOR MOVING PIECES, ONLY SUPPOSE TO BE USED TO CALCULATE POSSIBLE MOVES
    #IN OOP, THIS WOULD BE A PRIVATE FUNCTION
    #param: 
        square the piece is on
    #param: 
        it's new square
    #post: 
        makes the old square have no chesspiece, removes the piece on the new square from the game, 
        pChesspiece now linked to new square
    #return: 
        if the move is valid or not, aka, does it keep it out of check or not
    """
    def validatePossibleMove(self, pOldSquare, pNewSquare):
        newSquare = self._matrix[pNewSquare.getRank()][pNewSquare.getFile()]
        oldSquare = self._matrix[pOldSquare.getRank()][pOldSquare.getFile()]

        movedPiece = oldSquare.getChessPiece()

        oldSquare.removeChessPiece()

        self.removePieceFromChessBoard(newSquare)

        movedPiece.setSquare(newSquare)
        newSquare.setChessPiece(movedPiece)

        self.updateVisionAll()

        return not self.isTeamInCheck(movedPiece.getPieceAllegiance())
    
    #============================================================================================
    # Handeling the gameplay
    #============================================================================================

    #setup a board, then starts the game loop
    def playGameText(self):
        self.setUpChessBoard()

        play = True
        winner = None

        while play:
            self.updateVisionAll()
            self.updateValidMovesTeam(self._homeTurn)
            
            if self.isEnd(self._homeTurn):
                play = False
                if self.isTeamInCheck(self._homeTurn):
                    if self._homeTurn:
                        winner = self._vistorTeam
                    else:
                        winner = self._homeTeam

                break

            print("White to Play" if self._homeTurn else "Black to Play")
            self.printBoard()
            self.printTeamValidMoves(self._homeTurn)
            self.getPlayerMoveText()

            self._homeTurn = not self._homeTurn

            self.addToHistory()
            
        if winner == None:
            print("STALEMATE")
        else:
            print("WHITE WINS" if winner == self._homeTeam else "BLACK WINS")
            
            
    def getPlayerMoveText(self):

        firstSquare = None
        secondSquare = None

        validInput = False
        castle = None

        while not validInput:
            #input command in the form
            #square 'to'
            print("Give first square")
            firstSquare = input()

            print("Give second square")
            secondSquare = input()

            letterToFile = {'A' : 7, 'B' : 6, 'C' : 5, 'D' : 4, 'E' : 3, 'F' : 2, 'G' : 1, 'H' : 0} 

            firstSquare = self._matrix[int(firstSquare[1])-1][letterToFile[firstSquare[0]]]
            secondSquare = self._matrix[int(secondSquare[1])-1][letterToFile[secondSquare[0]]]
            
            # first condition for early invalid
            # if the first square doesnt have a piece, or if it doesnt match the turn
            if not firstSquare.hasChessPiece() or firstSquare.getChessPiece().getPieceAllegiance() != self._homeTurn:
                print("Invalid Input")
            #  or the pieces cant go to the second square
            elif not secondSquare in firstSquare.getChessPiece().getValidMoves():
                #caslte attempt if one is the king
                if isinstance(firstSquare.getChessPiece(), King):
                    #get the curr team
                    team = None

                    if self._homeTurn:
                        team = self._homeTeam
                    else:
                        team = self._vistorTeam

                    if secondSquare.getChessPiece() == team.getKingSideRook() or secondSquare == team.getKingSideRook().getKingDestination():
                        if self.canCastle(team.getKingSideRook()):
                            #castle
                            castle = team.getKingSideRook()
                            validInput = True
                            break
                    elif secondSquare.getChessPiece() == team.getQueenSideRook() or secondSquare == team.getQueenSideRook().getKingDestination():
                        if self.canCastle(team.getKingSideRook()):
                            #castle
                            castle = team.getQueenSideRook()
                            validInput = True
                            break
                print("Invalid Input")
            else:
                validInput = True

        if castle:
            #castle func
            self.performCastle(castle, firstSquare.getChessPiece())
        else:
            self.playerMove(firstSquare, secondSquare)

    #param: old square
    #param: new square
    def playerMove(self, pOldSquare, pNewSquare):
        movedPiece = pOldSquare.getChessPiece()

        pOldSquare.removeChessPiece()

        self.removePieceFromChessBoard(pNewSquare)

        movedPiece.setSquare(pNewSquare)
        pNewSquare.setChessPiece(movedPiece)

        movedPiece.increaseMoveCount()

        self.updateVisionAll()

    #pre: the current rook and king CAN caslte, do not use this function unless tested using can Castle function externally
    #param: the rook that is being castled
    #param: the king that is being castle
    #post: performs a castle
    def performCastle(self, pRook, pKing):
        pKing.getSquare().removeChessPiece()
        pRook.getSquare().removeChessPiece()

        pKing.setSquare(pRook.getKingDestination())
        pRook.getKingDestination().setChessPiece(pKing)

        pRook.setSquare(pRook.getRookDestination())
        pRook.getRookDestination().setChessPiece(pRook)

        pKing.increaseMoveCount()
        pRook.increaseMoveCount()

        self.updateVisionAll()



    #final game mechanic, winning/losing or a draw, so we need one function to check if it's the end
    #(no more valide moves), and we'll use isCheck in the playing the game function to see if it's
    #checkmate or stalemate
    #param: the team that is being checked for checkmate 
    #returns if they have no more valid moves
    def isEnd(self, pHome):
        team = None

        if pHome:
            team = self._homeTeam
        else:
            team = self._vistorTeam

        count = team.getAmountOfValidMoves()

        if self.canCastle(team.getKingSideRook()):
            count += 1
        
        if self.canCastle(team.getQueenSideRook()):
            count += 1

        if count > 0:
            return False
        
        return True
    

    #setup a board, then starts the game loop
    #this is the graphic version so no more text, or atleast this time it's going to be drawing at least
    def playGameGraphic(self):
        self.setUpChessBoard()

        play = True
        winner = None

        while play:
            self.updateVisionAll()
            self.updateValidMovesTeam(self._homeTurn)
            
            if self.isEnd(self._homeTurn):
                play = False
                if self.isTeamInCheck(self._homeTurn):
                    if self._homeTurn:
                        winner = self._vistorTeam
                    else:
                        winner = self._homeTeam

                break

            
            print("White to Play" if self._homeTurn else "Black to Play")

            #self.displayScreen()



            #self.printBoard()
            #self.printTeamValidMoves(self._homeTurn)
            
            self.getPlayerMoveGraphic()

            self._homeTurn = not self._homeTurn

            self.addToHistory()
            
        if winner == None:
            print("STALEMATE")
        else:
            print("WHITE WINS" if winner == self._homeTeam else "BLACK WINS")

    #============================================================================================
    # Handeling drawing the baord
    #============================================================================================

    #draw the baord from black's perspective
    #param: side length of chess board
    #param: tuple of x and y coord
    def drawBoardBlack(self, pLength, pCoords):
        #board =  pygame.image.load('assets/images/chessboardCom.png')
        board = pygame.transform.scale(self._NEUTRAL_IMAGE_URL['Board'], (pLength, pLength))
        self._screen.blit(board, pCoords)
        
        piece = None # pygame.image.load('assets/images/pawnRed.png')
        for i in range(8):
            for j in range(8):
                if not self._matrix[i][j].hasChessPiece():
                    continue
                
                
                piece = self._matrix[i][j].getChessPiece()
                
                currDictionary = None
                if piece.getPieceAllegiance():
                    currDictionary = self._PIECE_IMAGE_URL_RED
                else:
                    currDictionary = self._PIECE_IMAGE_URL_PURPLE

                if isinstance(piece, Pawn):
                    piece = currDictionary['Pawn']
                else:
                    piece = currDictionary['Rook']

                squareSize = pLength/8

                piece = pygame.transform.scale(piece, ((squareSize/8) * 7, (squareSize/8) *7))
                self._screen.blit(piece, (squareSize*j + squareSize/16 + pCoords[0], squareSize*i + squareSize/16 + pCoords[1]))
                

    #
    def displayScreen(self):
        self._screen.fill((0,0,0))
        #14, 219, 248)

        self.drawBoardBlack(self._BLACK_BOARD_LENGTH, self._BLACK_BOARD_COORDINATES)

        pygame.display.update()
        self._clock.tick(60)

    def getPlayerMoveGraphic(self):
        selectedSquare = None
        firstSquare = None
        secondSquare = None

        validInput = False
        castle = None

        #get the curr team
        team = None

        if self._homeTurn:
            team = self._homeTeam
        else:
            team = self._vistorTeam


        while not validInput:
            self.displayScreen()
            #input command in the form
            #square 'to'
            """
            print("Give first square")
            firstSquare = input()

            print("Give second square")
            secondSquare = input()

            letterToFile = {'A' : 7, 'B' : 6, 'C' : 5, 'D' : 4, 'E' : 3, 'F' : 2, 'G' : 1, 'H' : 0} 

            firstSquare = self._matrix[int(firstSquare[1])-1][letterToFile[firstSquare[0]]]
            secondSquare = self._matrix[int(secondSquare[1])-1][letterToFile[secondSquare[0]]]
            """
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.dict['pos'])
                    withinBlackX = event.dict['pos'][0] > self._BLACK_BOARD_COORDINATES[0] and event.dict['pos'][0] < self._BLACK_BOARD_COORDINATES[0] + self._BLACK_BOARD_LENGTH
                    withinBlackY = event.dict['pos'][1] > self._BLACK_BOARD_COORDINATES[1] and event.dict['pos'][1] < self._BLACK_BOARD_COORDINATES[1] + self._BLACK_BOARD_LENGTH
                    #if it's clicked on the blackboard, we get the square using black orientation
                    if withinBlackX and withinBlackY:
                        rank = (event.dict['pos'][1] - self._BLACK_BOARD_COORDINATES[1])//(self._BLACK_BOARD_LENGTH//8)
                        file = (event.dict['pos'][0] - self._BLACK_BOARD_COORDINATES[0])//(self._BLACK_BOARD_LENGTH//8)
                        selectedSquare = self._matrix[rank][file]
                        
                        #if there's no current first square, the selected square is immedietly that one
                        if not firstSquare:
                            #if selected square is has a piece on the team
                            if selectedSquare.hasChessPiece() and selectedSquare.getChessPiece().getPieceAllegiance() == self._homeTurn:
                                firstSquare = selectedSquare
                            #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                        elif selectedSquare == firstSquare:
                            firstSquare = None
                            #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                        #everything after this assumes first square has a value
                        #so the first things to check for if the person is trying unselect, (picking an empty square), this is also 
                        #how u castle tho, so u must check for that as welll
                        #we also have to see if they're trying to jump to an empty square
                        elif not selectedSquare.hasChessPiece():
                            #if the piece on the first square is a king, we may check for castle, else, it's an unselect
                            #invert this idea for early exit
                            if not isinstance(firstSquare.getChessPiece(), King):
                                if selectedSquare in firstSquare.getChessPiece().getValidMoves():
                                    secondSquare = selectedSquare
                                    validInput = True
                                    #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                                    continue

                                firstSquare = None
                                secondSquare = None
                                #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                                continue
                            
                            #everything from this point assumes it's a king
                            if selectedSquare == team.getKingSideRook().getKingDestination():
                                if self.canCastle(team.getKingSideRook()):
                                    #castle
                                    castle = team.getKingSideRook()
                                    validInput = True
                                    #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                                    continue
                                #secondSquare = team.getKingSideRook().getSquare()

                            if selectedSquare == team.getQueenSideRook().getKingDestination():
                                if self.canCastle(team.getQueenSideRook()):
                                    #castle
                                    castle = team.getQueenSideRook()
                                    validInput = True
                                    #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                                    continue
                                
                                #secondSquare = team.getQueenSideRook().getSquare()


                            firstSquare = None
                            secondSquare = None
                            #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                            continue

                        elif selectedSquare.hasChessPiece():
                            

                            if selectedSquare.getChessPiece().getPieceAllegiance() == self._homeTurn:
                                firstSquare = selectedSquare
                                #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                                continue

                            if selectedSquare in firstSquare.getChessPiece().getValidMoves():
                                secondSquare = selectedSquare
                                validInput = True
                                #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                                continue

                            firstSquare = None
                            secondSquare = None
                            #self.testFunction(selectedSquare, firstSquare, secondSquare, castle)
                            continue

        print("test speed")
        if castle:
            #castle func
            self.performCastle(castle, firstSquare.getChessPiece())
        else:
            self.playerMove(firstSquare, secondSquare)
        print("vroomm")
        self.displayScreen()
        print("skrrrrt")


    def testFunction(self, selectedSquare, firstSquare, secondSquare, castle):
        print("board", selectedSquare.getLocation())
        print("first square:", firstSquare.getLocation() if firstSquare else "None")
        if not castle:
            print("second square:", secondSquare.getLocation() if secondSquare else "None")
        else:
            print("caslte:", castle.getSquareLocation())

        

