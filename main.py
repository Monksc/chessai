import game
import aiagents
import chess


if __name__ == "__main__":
    g = game.Game(aiagents.createMiniMaxAIAgent(chess.WHITE, 3, 0.1), aiagents.createMiniMaxAIAgent(chess.BLACK, 3, 0.1))

    print("WHITE WINS!" if g.playGame() else "BLACK WINS!")
