import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
import sys
import random
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, QWidget,
    QPushButton, QLabel, QGridLayout)
import chess
import aiagents

class Board(QWidget):
    def __init__(self, player1=None, player2=None, board=chess.Board()):
        QWidget.__init__(self)

        self.lastClicked = None
        self.board = board
        self.player1 = player1
        self.player2 = player2

        self.fowardmoves = []

        self.layout = QGridLayout()
        self.setWindowTitle("WHITE")

        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                self.buttons[r][c] = QPushButton("HELLO")
                self.updateTile(r, c, False)
                self.buttons[r][c].clicked.connect(self.clickedTile(r, c))
                self.layout.addWidget(self.buttons[r][c], r, c)


        goagainbtn = QPushButton("AI Go Again")
        goagainbtn.clicked.connect(self.takeAITurn)
        self.layout.addWidget(goagainbtn, 8, 0)

        backbtn = QPushButton("<")
        backbtn.clicked.connect(self.gobackonemove)
        self.layout.addWidget(backbtn, 8, 4)

        fwdbtn = QPushButton(">")
        fwdbtn.clicked.connect(self.gofwdonemove)
        self.layout.addWidget(fwdbtn, 8, 5)

        self.setLayout(self.layout)

        self.takeAITurn()

    def refreshboard(self):
        for r in range(8):
            for c in range(8):
                self.updateTile(r, c, False)

    def gobackonemove(self):
        self.fowardmoves.append(self.board.pop())
        self.refreshboard()
    def gofwdonemove(self):
        if len(self.fowardmoves) > 0:
            self.board.push(self.fowardmoves[0])
            del self.fowardmoves[0]
            self.refreshboard()

    def takeAITurn(self):
        player = self.player1 if self.board.turn else self.player2
        if player is None:
            return
        move = player(self.board, self.board.generate_legal_moves())
        self.makeMove(move)

    def rowsToIndex(self, row, col):
        return (7 - row) * 8 + col
    def indexToRows(self, index):
        return (7 - (index // 8), index % 8)

    def updateTile(self, row, col, isClicked):
        text = str(self.board.piece_at(self.rowsToIndex(row, col)))
        if text == "None":
            text = ""
        if isClicked:
            text += "CLICKED"
        self.buttons[row][col].setText(text)


    def makeMove(self, move):
        if not(self.board.is_legal(move)):
            # default promote queen
            if not(move is None):
                move.promotion = 5
        if self.board.is_legal(move):
            self.board.push(move)
            self.fowardmoves = []
            self.refreshboard()

        if self.board.is_game_over():
            if self.board.is_checkmate():
                self.setWindowTitle("BLACK WINS!!!" if self.board.turn else "WHITE WINS!!!")
            else:
                self.setWindowTitle("TIE")
        else:
            self.setWindowTitle("WHITE" if self.board.turn else "BLACK")
            self.takeAITurn()

        r, c = self.indexToRows(move.from_square)
        self.updateTile(r, c, False)
        r, c = self.indexToRows(move.to_square)
        self.updateTile(r, c, False)


    def makePersonMove(self, fromRC, toRC):
        player = self.player1 if self.board.turn else self.player2
        if not(player is None):
            return

        m1 = self.rowsToIndex(fromRC[0], fromRC[1])
        m2 = self.rowsToIndex(toRC[0], toRC[1])
        move = chess.Move(m1, m2)
        self.makeMove(move)



    def clickedTile(self, row, col):
        def f():
            if self.lastClicked is None:
                self.lastClicked = (row, col)
                self.updateTile(row, col, True)
                return

            r, c = self.lastClicked

            if not(row == r and col == c):
                self.makePersonMove((r, c), (row, col))
                self.updateTile(r, c, False)

            self.updateTile(row, col, False)
            self.lastClicked = None

        return f


if __name__ == "__main__":
    app = QApplication(sys.argv)

    #widget = Board(aiagents.createMiniMaxAIAgent(chess.WHITE, 2, 0.1))
    widget = Board(None, aiagents.createMiniMaxAIAgent(chess.BLACK, 2, 0.1))
    # widget = Board(aiagents.createMiniMaxAIAgent(chess.WHITE, 2, 0.25), aiagents.createMiniMaxAIAgent(chess.BLACK, 2, 0.25))
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())

