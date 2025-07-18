# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        nearestGhostDistance = min(manhattanDistance(newGhostState.getPosition(), newPos) for newGhostState in newGhostStates)
        if nearestGhostDistance == 0:
            return 0
        foodDistances = [manhattanDistance(newPos, (x, y)) for x in range(newFood.width) for y in range(newFood.height) if newFood[x][y]]
        if newFood.count(True) == currentGameState.getFood().count(True):
            foodValue = -min(foodDistances)
        else:
            foodValue = max(newFood.width, newFood.height)
        return successorGameState.getScore() - 5 / nearestGhostDistance + foodValue

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

def minimax(gameState: GameState, depth, evaluationFunction, agentIndex):
    if depth == 0 or gameState.isWin() or gameState.isLose():
        return evaluationFunction(gameState), None
    strategies = []
    for action in gameState.getLegalActions(agentIndex):
        newState = gameState.generateSuccessor(agentIndex, action)
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
        strategies.append((minimax(newState, depth - (nextAgentIndex == 0), \
                                   evaluationFunction, nextAgentIndex)[0], action))
    if agentIndex == 0:
        return max(strategies, key = lambda x: x[0])
    else:
        return min(strategies, key = lambda x: x[0])

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return minimax(gameState, self.depth, self.evaluationFunction, 0)[1]

import math

def alphabeta(gameState: GameState, depth, evaluationFunction, agentIndex, alpha = -math.inf, beta = math.inf):
    if depth == 0 or gameState.isWin() or gameState.isLose():
        return evaluationFunction(gameState), None
    if agentIndex == 0:
        ret = (-math.inf, None)
        for action in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            newEval = alphabeta(newState, depth - (nextAgentIndex == 0), \
                                evaluationFunction, nextAgentIndex, alpha, beta)[0]
            alpha = max(alpha, newEval)
            if newEval > ret[0]:
                ret = (newEval, action)
            if alpha > beta:
                break
        return ret
    else:
        ret = (math.inf, None)
        for action in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            newEval = alphabeta(newState, depth - (nextAgentIndex == 0), \
                                evaluationFunction, nextAgentIndex, alpha, beta)[0]
            beta = min(beta, newEval)
            if newEval < ret[0]:
                ret = (newEval, action)
            if alpha > beta:
                break
        return ret

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return alphabeta(gameState, self.depth, self.evaluationFunction, 0)[1]

def expectimax(gameState: GameState, depth, evaluationFunction, agentIndex):
    if depth == 0 or gameState.isWin() or gameState.isLose():
        return evaluationFunction(gameState), None
    strategies = []
    for action in gameState.getLegalActions(agentIndex):
        newState = gameState.generateSuccessor(agentIndex, action)
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
        strategies.append((expectimax(newState, depth - (nextAgentIndex == 0), \
                                   evaluationFunction, nextAgentIndex)[0], action))
    if agentIndex == 0:
        return max(strategies, key = lambda x: x[0])
    else:
        return sum(map(lambda x: x[0], strategies)) / len(strategies), None

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return expectimax(gameState, self.depth, self.evaluationFunction, 0)[1]

def step(pos0, pos1):
    newPos = [(pos0[0] + dx, pos0[1] + dy) for dx, dy in ((1, 0), (0, 0), (0, 1), (1, 1))]
    return min(newPos, key = lambda pos: (pos[0] - pos1[0]) ** 2 + (pos[1] - pos1[1]) ** 2)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    wall = currentGameState.getWalls()
    foodPositions = [(x, y) for x in range(food.width) for y in range(food.height) if food[x][y]]
    foodDistances = [manhattanDistance(pos, t) / float(food.width + food.height) for t in foodPositions]
    if len(foodDistances) >= 1:
        if min(foodDistances) < .25:
            distanceCorrection = -min(foodDistances)
        else:
            distanceCorrection = -sum(foodDistances) / len(foodDistances)
        minDistanceIndex = foodDistances.index(min(foodDistances))
        stepx, stepy = step(pos, foodPositions[minDistanceIndex])
        wallPenalty = -wall[stepx][stepy] / (2 * (food.width + food.height))
    else:
        distanceCorrection = 0
        wallPenalty = 0
    return currentGameState.getScore() + distanceCorrection + wallPenalty

# Abbreviation
better = betterEvaluationFunction
