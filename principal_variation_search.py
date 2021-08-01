import math
import time

class PVS:
    def __init__(self, minDepth, startTime, totalTime, isTerminal, calculateScore, getMoves, doMove, undoMove, quickHash):
        self.minDepth = minDepth
        self.startTime = startTime
        self.totalTime = totalTime
        self.isTerminal = isTerminal
        self.calculateScore = calculateScore
        self.getMoves = getMoves
        self.doMove = doMove
        self.undoMove = undoMove
        self.quickHash = quickHash

    def pvs(self, node, depth, a, b, color, cacheScore):

        if depth == 0 or self.isTerminal(node) or (depth % 2 == 0 and depth <= self.minDepth and time.time() - self.startTime > self.totalTime):
            score = self.calculateScore(node, color)
            cacheScore[self.quickHash(node)] = score
            return None, score

        if self.quickHash(node) in cacheScore:
            return None, cacheScore[self.quickHash(node)]

        score = None
        bestAction = None

        for action in self.getMoves(node, depth, a, b):
            child = self.doMove(node, action)
            if score == None:
                score = -self.pvs(child, depth -1, -b, -a, -color, cacheScore)[1]
            else:
                score = -self.pvs(child, depth -1, -a-1, -a, -color, cacheScore)[1]

                if a < score and score < b:
                    score = -self.pvs(child, depth -1, -b, -score, -color, cacheScore)[1]

            self.undoMove(child, action)

            if score > a:
                a = score
                bestAction = action

            if a > b:
                break

        return bestAction, a


def pvs(node, minDepth, maxDepth, totalTime, color, isTerminal, calculateScore, getMoves, doMove, undoMove, quickHash):

    p = PVS(minDepth*2, time.time(), totalTime, isTerminal, calculateScore, getMoves, doMove, undoMove, quickHash)
    return p.pvs(node, maxDepth*2, -math.inf, math.inf, color, {})



if __name__ == "__main__":

    def isTerminal(x):
        return False

    def calculateScore(x, color):
        return x * color

    def nextNodes(x):
        yield ("UP", x+0.5)
        yield ("SAME", x)
        yield ("DOWN", x-1)
        yield ("NEGATE", -x)

    def getMoves(x):
        yield "UP"
        yield "SAME"
        yield "DOWN"
        yield "NEGATE"

    def doMove(x, move):
        if move == "UP": return x+0.5
        if move == "SAME": return x
        if move == "DOWN": return x-1
        if move == "NEGATE": return -x

    def undoMove(x, move):
        if move == "UP": return x-0.5
        if move == "SAME": return x
        if move == "DOWN": return x+1
        if move == "NEGATE": return -x
    
    for i in range(6):
        print(i, pvs(-100, i, 1, isTerminal, calculateScore, getMoves, doMove, undoMove))

