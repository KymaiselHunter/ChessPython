# main.py
from chessboard import Chessboard

print("Hello World")

#testing display + adding a random thingy
testBoard = Chessboard()

#testBoard.testSet()
#removed, must make new function that will add a piece to the board, then test it using its other functions

#testBoard.displayBoard()

#testing clearing the board
#testBoard.clearBoard()
#testBoard.displayBoard()

#testing the defualt creation
testBoard.setUpChessBoard()
testBoard.updateVisionAll()
print("White In Check?", testBoard.isTeamInCheck(True))
print("Black In Check?", testBoard.isTeamInCheck(False))
testBoard.printBoard()

testBoard.printTeamVision(True)
testBoard.printTeamVision(False)



testBoard.testFunc3()


testBoard.updateVisionAll()
print("White In Check?", testBoard.isTeamInCheck(True))
print("Black In Check?", testBoard.isTeamInCheck(False))
testBoard.printBoard()

testBoard.printTeamVision(True)
testBoard.printTeamVision(False)
