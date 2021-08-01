import chess
import game
import minimax
import principal_variation_search as pvs
import basicScore
import random
import math
import time

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

def createPVS(color, minDepth=2, maxDepth=3, totalTime=30.0, probRandom=0.2):

    def isTerminal(board):
        return board.is_game_over()

    # Should return a value from 0 - 1
    def calculatePositioning(state, piece_type, position):

        row = position // 8
        col = position % 8

        # Rook, Queen or King
        if piece_type >= 4:
            return ((row - 3.5)**2 + (3.5 - abs(3.5 - col)) / 2.0) / 14.0

        # Bishop
        if piece_type == 3:
            if state.turn:
                if row == 7:
                    return 1.0
                return 0.0
            else:
                if row == 0:
                    return 1.0
                return 0.0

        # Night
        if piece_type == 2:
            row = abs(3.5 - row)
            col = abs(3.5 - col)
            return (1.0 - ((row)**0.1 + (col)**0.1) / (2*3.5**0.1)) / 0.824

        # Night
        if piece_type == 1:
            if col <= 4:
                if state.turn:
                    return (col + row) / 11.0
                else:
                    return (col - row) / 11.0
            else:
                if state.turn:
                    return -row / 7.0
                else:
                    return row / 7.0

        return 0


    def calculateMoveScore(state, move):
        worth = [0, 1, 9, 27, 81, 250, 500]
        #worth = [0, 1, 4, 3, 9, 16, 50]
        piece = state.piece_at(move.from_square)
        color = piece.color * 2 - 1

        score = 0.0
        piece_type = piece.piece_type
        if move.promotion != None:
            score += worth[move.promotion] - worth[1]
            piece_type = move.promotion

        score -= calculatePositioning(state, piece_type, move.from_square)
        score += calculatePositioning(state, piece_type, move.to_square)


        piece = state.piece_at(move.to_square)
        if piece == None: return color * score

        score -= calculatePositioning(state, piece.piece_type, move.to_square)
        return color * (worth[piece.piece_type] + score)
        
    def getMoves(state, depth, a, b):
        return state.legal_moves

    def getMovesSorted(state, depth, a, b):
        if depth <= 2:
            for move in state.legal_moves:
                yield move
            return

        mid = (a + b) / 2
        if math.isfinite(mid):
            mid = 0

        moves = state.legal_moves
        scoreAndMove = []
        for move in moves:
            board = state.copy()
            scoreAndMove.append((calcScore(state, 1.0) + calculateMoveScore(state, move), move))

        scoreAndMove.sort(key=lambda x: x[0], reverse=state.turn)
        for move in scoreAndMove:
            yield move[1]

    def doMove(state, move):
        score = calculateMoveScore(state, move)
        state.san_and_push(move)
        state.score += score
        return state
    def undoMove(state, move):
        state.pop()
        score = calculateMoveScore(state, move)
        state.score -= score
        return state

    def calcScore(board, color):
        if board.is_game_over():
            if board.is_checkmate():
                return -10_000
            return 0

        return board.score * color

    def quickHash(state):
        return state.pawns ^ state.knights ^ state.bishops ^ state.rooks ^ state.queens ^ state.kings + state.turn
        

    def f(board, moves):
        if random.random() < probRandom:
            return randomMove(board, moves)

        board.score = 0

        action, score = pvs.pvs(board, minDepth, maxDepth, totalTime, board.turn * 2 - 1, isTerminal, calcScore, getMovesSorted, doMove, undoMove, quickHash)
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

