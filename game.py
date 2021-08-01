import chess
import numpy as np
import random
import time
import basicScore
import aiagents


class Game:
    def __init__(self, whiteAgent, blackAgent):
        self.whiteAgent = whiteAgent
        self.blackAgent = blackAgent
        self.board = chess.Board()

    def __str__(self):
        return str(self.board.mirror())#.unicode()

    def __repr__(self):
        return self.board.mirror().unicode()

    def getAgent(self):
        if self.board.turn:
            return self.whiteAgent
        return self.blackAgent

    def playTurn(self):
        agent = self.getAgent()
        board = self.board.copy()
        moves = board.legal_moves
        if moves.count() == 0:
            return False


        start = time.time()
        move = agent(board, moves)
        print("White" if board.turn else "Black", "Time: %.2fs" % (time.time() - start))

        self.board.san_and_push(move)
        return True

    def playGame(self):
        print(self)
        while not(self.board.is_game_over()):
        #while True: #for i in range(50):
            if not self.playTurn():
                print("WHITE DID BETTER!" if not(self.board.turn) else "BLACK DID BETTER")
                return 0 # Tie
            print("\n" * 2)
            print(self)
            
            if self.board.is_checkmate():
                if self.board.turn:
                    return -1
                else:
                    return 1

            #if self.board.turn:
            #    input()

        print("MADE IT TO END")
        white, black = basicScore.calculateScore(self.board)
        print(white, black)
        return 0

        # if white > black:
        #     return 1
        # elif white == black:
        #     return 0
        # else:
        #     return -1

if __name__ == "__main__":
    #g = Game(aiagents.createMiniMaxAIAgent(chess.WHITE, 2, 0.1), aiagents.createMiniMaxAIAgent(chess.WHITE, 1, 0.5))
    g = Game(aiagents.createPVS(chess.WHITE, 1, 3, 15.0, 0.0), aiagents.createMiniMaxAIAgent(chess.BLACK, 2, 1.0))
    #g = Game(aiagents.createMiniMaxAIAgent(chess.WHITE, 2, 0.1), aiagents.createPVS(chess.BLACK, 2, 3, 5.0, 0.0))
    #g = Game(aiagents.createMiniMaxAIAgent(chess.WHITE, 2, 0.0), aiagents.bestScore(chess.BLACK, 1.0))
    index = g.playGame()
    winner = ["BLACK WINS!!!", "TIE!!!", "WHITE WINS!!!"][index+1]
    print(winner)


