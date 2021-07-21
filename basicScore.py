import chess
import numpy as np

def howMany1Bits(x):
    count = 0
    while x > 0:
        x = (x & (x-1))
        count += 1
    return count

def calculateScore(board):
    whitePieces, blackPieces = getPieceCountArray(board)

    # _ Pawn, Knight, Bishop, Rook, Queen, King
    worth = np.array([0, 1, 9, 27, 81, 250, 500])
    whiteScore = worth @ np.array(whitePieces)
    blackScore = worth @ np.array(blackPieces)

    return (whiteScore, blackScore)

def getPieceCountArray(board):
    whitePieces = [0 for _ in range(len(chess.PIECE_NAMES))]
    blackPieces = [0 for _ in range(len(chess.PIECE_NAMES))]

    for i in range(64):
        piece = board.piece_at(i)
        if piece is None:
            continue
        if piece.color:
            whitePieces[piece.piece_type] += 1
        else:
            blackPieces[piece.piece_type] += 1
    
    return whitePieces, blackPieces

def getAttackedByArray(color):
    pieces = [0 for _ in range(len(chess.PIECE_NAMES))]

    for i in range(64):
        if board.is_attacked_by(color, i):
            pieces[board.piece_at(i).piece_type] += 1

        piece = board.piece_at(i)
        if piece is None:
            continue
        if piece.color:
            whitePieces[piece.piece_type] += 1
        else:
            blackPieces[piece.piece_type] += 1

    # _ Pawn, Knight, Bishop, Rook, Queen, King
    worth = np.array([0, 1, 9, 27, 81, 250, 500])
    whiteScore = worth @ np.array(whitePieces)
    blackScore = worth @ np.array(blackPieces)

    return (whiteScore, blackScore)


