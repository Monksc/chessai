import random
import minimax
from enum import Enum
class Tile(Enum):
    EMPTY = " "
    X = "X"
    O = "O"

def randomAi(board):
    r = random.randint(0,2)
    c = random.randint(0,2)
    return r, c

def playerTurn(board):
    print(board)
    while True:
        try:
            initialinput = input("Take a turn: ")
            move = int(initialinput) - 1
            if move < 0 or move > 8:
                continue

            r = move // 3
            c = move % 3
            return r, c
        except:
            print(initialinput)
            print(initialinput == "^C")
            print("OOPSIES!! Try again. This time type an integer from [1 - 9]")

def minimaxAi(player):

    def nextStates(board, isMax):

        winner = board.checkForWinner()
        if winner == player:
            yield (board.copy(), "FOO")
            return
        elif winner != Tile.EMPTY:
            yield (board.copy(), "BAR")
            return

        y = False
        for move in range(9):
            b = board.copy()

            r = move // 3
            c = move % 3

            if b.takeTurn(r, c):
                y = True
                yield (b, move)

        if not(y):
            yield (board.copy(), "TIE")
            return

    def calcScore(board):
        winner = board.checkForWinner()
        if winner == Tile.EMPTY:
            return 0
        elif winner == player:
            return 1
        else:
            return -1


    def f(board):
        move = minimax.minimax(board, nextStates, calcScore, roundsLeft=5)[1]
        return (move // 3, move % 3)

    return f


class TicTacToe:

    def __init__(self):
        self.board = [[Tile.EMPTY] * 3 for i in range(3)]
        self.turns = 0

    def __str__(self):
        rstr = ""
        for r in range(3):
            if r > 0:
                rstr += "\n" + ("-" * 9) + "\n"
            for c in range(3):
                if c > 0:
                    rstr += " | "
                rstr += self.board[r][c].value
        return rstr

    def __repr__(self):
        return str(self)

    def copy(self):
        b = TicTacToe()
        b.board = [[self.board[r][c] for c in range(3)] for r in range(3)]
        b.turns = self.turns
        return b

    def getPlayersTurn(self):
        return list(Tile)[(self.turns % 2) + 1]


    def takeTurn(self, r, c):
        if self.board[r][c] == Tile.EMPTY:
            self.board[r][c] = self.getPlayersTurn()
            self.turns += 1
            return True
        return False

    def checkForAllTheSame(self, row, tile):
        for r in row:
            if r != tile:
                return False
        return True

    def checkRow(self, row, tile):
        return self.checkForAllTheSame(self.board[row], tile)

    def checkCol(self, col, tile):
        return self.checkForAllTheSame([
                self.board[0][col],
                self.board[1][col],
                self.board[2][col],
            ], tile)

    def checkIfTileWon(self, tile):
        for i in range(3):
            if self.checkRow(i, tile) or self.checkCol(i, tile):
                return True

        return self.checkForAllTheSame([
                self.board[0][0],
                self.board[1][1],
                self.board[2][2],
            ], tile) or self.checkForAllTheSame([
                self.board[2][0],
                self.board[1][1],
                self.board[0][2],
            ], tile)

    def checkForWinner(self):
        for i in range(1,3):
            player = list(Tile)[i]
            if self.checkIfTileWon(player):
                return player
        return Tile.EMPTY

    def playGame(self, xturn, oturn):
        while self.turns < 9:
            r, c = ([xturn, oturn][self.turns % 2])(self)
            self.takeTurn(r, c)
            winner = self.checkForWinner()
            if winner != Tile.EMPTY:
                return winner

        return Tile.EMPTY


def playGame(player1, player2):
    b = TicTacToe()
    winner = b.playGame(player1, player2)
    if winner == Tile.EMPTY:
        print("TIE!!!")
    else:
        print(winner.value, "WON!!!!")

    print(b)


if __name__ == "__main__":
    # playGame(minimaxAi(Tile.X), randomAi)
    # playGame(minimaxAi(Tile.X), minimaxAi(Tile.O))
    playGame(minimaxAi(Tile.X), playerTurn)
    # playGame(playerTurn, minimaxAi(Tile.O))

