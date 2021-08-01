import game
import aiagents
import chess


if __name__ == "__main__":
    g = game.Game(aiagents.createMiniMaxAIAgent(chess.WHITE, 3, 0.1), aiagents.createMiniMaxAIAgent(chess.BLACK, 3, 0.1))
    #g = game.Game(aiagents.createPVS(chess.WHITE, 2, 0.0), aiagents.createMiniMaxAIAgent(chess.BLACK, 1, 1.0))

    print("WHITE WINS!" if g.playGame() else "BLACK WINS!")
