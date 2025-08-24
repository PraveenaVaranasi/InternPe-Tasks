import random
ROWS = 6
COLS = 7
gameBoard = [[" " for _ in range(COLS)] for _ in range(ROWS)]
def printGameBoard():
    print("\n    A    B    C    D    E    F    G")
    for r in range(ROWS):
        print("  +----+----+----+----+----+----+----+")
        print(r, "|", end="")
        for c in range(COLS):
            print(" " + gameBoard[r][c] + " ", end="|")
        print()
    print("  +----+----+----+----+----+----+----+")
def dropPiece(col, piece):
    for r in range(ROWS - 1, -1, -1):  # Start from bottom row
        if gameBoard[r][col] == " ":
            gameBoard[r][col] = piece
            return True
    return False  # if the column is full
def checkWin(piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(gameBoard[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(gameBoard[r+i][c] == piece for i in range(4)):
                return True
# Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(gameBoard[r+i][c+i] == piece for i in range(4)):
                return True
# Diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(gameBoard[r-i][c+i] == piece for i in range(4)):
                return True
    return False
# Main game 
def playGame():
    print("Welcome to Connect Four! 🔴🟡")
    players = ["🔴", "🟡"]
    turn = 0
    while True:
        printGameBoard()
        player = players[turn % 2]
        move = input(f"Player {player}, choose a column (A-G): ").upper()
        if move not in "ABCDEFG":
            print("Invalid move. Try again.")
            continue
        col = ord(move) - ord("A")
        if not dropPiece(col, player):
            print("Column full! Try again.")
            continue
        if checkWin(player):
            printGameBoard()
            print(f"🎉 Player {player} WINS! 🎉")
            break
        # to Check draw
        if all(gameBoard[0][c] != " " for c in range(COLS)):
            printGameBoard()
            print("It's a DRAW! 🤝")
            break
        turn += 1
playGame()
