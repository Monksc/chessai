import math
import numpy as np

def minimax(state, nextStates, calcScore, roundsLeft=3, rangeMin=-math.inf, rangeMax=math.inf):

    if roundsLeft == 0:
        return (state, None, calcScore(state))

    # Max
    maxValue = -9999
    maxState = None
    maxAction = None
    for (newMaxState, action) in nextStates(state, True):

        # Min
        minValue = 99999
        minState = None
        newRangeMax = rangeMax
        for (newMinState, _) in nextStates(newMaxState, False):
            newState, _, newScore = minimax(newMinState, nextStates, calcScore, roundsLeft-1, rangeMin, newRangeMax)
            if newScore < minValue:
                minValue = newScore
                minState = newState

                if minValue < newRangeMax:
                    newRangeMax = minValue
                    if newRangeMax <= rangeMin:
                        #return (minState, action, minValue)
                        break

        if minValue > maxValue:
            maxValue = minValue
            maxState = minState
            maxAction = action

            if minValue > rangeMin:
                rangeMin = minValue
                if rangeMax <= rangeMin:
                    return (maxState, maxAction, maxValue)

    return (maxState, maxAction, maxValue)


def miniMaxTest(values=[(3, "RIGHT"), (5, "LEFT"), (6, "UP")]):
    def getNextStates(values, isMax):
        if type(values) == type(0):
            return [(values, None)]
        return values

    def calcScore(values):
        print("Calc score: ", values)
        return values
        #return np.array(values).max()

    return minimax(values, getNextStates, calcScore, 1)

def miniMaxTest2():
    state = {
        "value": 0,
        "children": [
            ({
                "value": 0,
                "children": [
                    ({
                        "value": 6,
                        "children": [],
                    }, "Down"),
                ]
            }, "Left"),
            ({
                "value": 0,
                "children": [
                    ({
                        "value": 2,
                        "children": [],
                    }, "Up"),
                    ({
                        "value": 4,
                        "children": [],
                    }, "Right")
                ]
            }, "South"),
        ],
    }

    def getNextStates(state, isMax):
        children = state["children"]
        if len(children) == 0:
            return [(state, "IDK")]
        return children

    def calcScore(values):
        return values["value"]

    return minimax(state, getNextStates, calcScore, 1)


if __name__ == "__main__":
    # print(miniMaxTest())
    print(miniMaxTest2())


