import chess
import game
import minimax
import basicScore
import random

def createMiniMaxAIAgent(color, movesAhead=3, probRandom=0.2):

    def nextState1(state, isMax):
        moves = state.legal_moves
        for move in moves:
            board = state.copy()
            board.san_and_push(move)
            yield (board, move)

    def nextState2(state, isMax):
        moves = state.legal_moves
        newStates = []
        for move in moves:
            board = state.copy()
            board.san_and_push(move)
            newStates.append((calcScore(board), (board, move)))

        newStates.sort(key=lambda x: x[0], reverse=not(isMax))
        for move in newStates:
            yield move[1]

    def calcScore(board):
        white, black = basicScore.calculateScore(board)

        if color:
           #return white / (white + black)
           return white - black
        #return black / (white + black)
        return black - white
        

    def f(board, moves):
        if random.random() < probRandom:
            return randomMove(board, moves)

        state, action, score = minimax.minimax(board, nextState1, calcScore, movesAhead)
        return action

    return f


def bestScore(color, chanceRand=0.1):
    def f(board, moves):
        if random.random() < chanceRand:
            return randomMove(board, moves)

        bestScore = -999999
        bestMove = None
        for m in moves:
            b = board.copy()
            b.san_and_push(m)
            white, black = basicScore.calculateScore(b)
            score = (white - black) / (white + black)
            if score > bestScore:
                bestScore = score
                bestMove = m
        return bestMove
    return f



# MARK: Random
def randomMove(board, moves):
    return random.choice(list(moves))

