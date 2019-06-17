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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        oldFood = currentGameState.getFood()
        currentPos = currentGameState.getPacmanPosition()
        currentGhostStates = currentGameState.getGhostStates()
        chased = False
        chasedBy = None
        for i in range(len(currentGhostStates)):
            if newScaredTimes[i] == 0:
                dis = manhattanDistance(currentPos, currentGhostStates[i].configuration.pos)
                if dis < 3:
                    chased = True
                    chasedBy = i

        capsules = currentGameState.getCapsules()

        if chased:
            for i in range(len(capsules)):
                dis = manhattanDistance(newPos, capsules[i])
                if dis == 0:
                    return float("inf")
            return manhattanDistance(newPos, currentGhostStates[chasedBy].configuration.pos)

        direction = self.nextToFood(oldFood, currentPos)
        if direction and direction == action:
            return float("inf")

        goalFood = self.findGoalFood(newFood)
        if not goalFood:
            raise Exception
        dis = manhattanDistance(newPos, goalFood)
        return 1 / dis

    def nextToFood(self, oldFood, currentPos):
        """
        Check whether currentPos is next to a food position. Returns the action that algorithm should perform
        :param oldFood: the grid of food
        :param currentPos:
        :return: string
        """
        if oldFood.data[currentPos[0] + 1][currentPos[1]]:
            return "East"
        elif oldFood.data[currentPos[0] - 1][currentPos[1]]:
            return "West"
        elif oldFood.data[currentPos[0]][currentPos[1] + 1]:
            return "North"
        elif oldFood.data[currentPos[0]][currentPos[1] - 1]:
            return "South"
        return None

    def findGoalFood(self, newFood):
        """
        Find the next food that should be chased.
        :param newFood: the food grid
        :return: the position of the food desired as tuple.
        """
        x = y = 0
        width = len(newFood.data)
        height = len(newFood.data[0])
        while x != width:
            if newFood[x][y]:
                return (x, y)
            y += 1
            if y == height:
                x += 1
                y = 0
        return None


def scoreEvaluationFunction(currentGameState):
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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        root = MinimaxNode(gameState, 0, 1, self.depth, self.evaluationFunction)
        return root.bestAction()


class MinimaxNode:
    """
    Node for minimax
    """

    def __init__(self, gameState, agentIndex, depth, maxDepth, evalFn):
        self.evalFn = evalFn
        self.maxDepth = maxDepth
        self.depth = depth
        self.gameState = gameState
        self.agentIndex = agentIndex
        self.numAgents = gameState.getNumAgents()

    def bestAction(self):
        """
        Finds the best action of the current node
        :return: the best action
        """
        scoresTuple = (0, float("-inf"))  # (action, score)
        for item in self.getChildrenWithAction():
            # item: (action, node)
            itemScore = item[1].getScore()
            if scoresTuple[1] <= itemScore:
                scoresTuple = (item[0], itemScore)
        return scoresTuple[0]

    def generateChildNode(self, action):
        """
        Generate the child node by the action applied
        :param action: the action that parent state applied
        """
        childState = self.gameState.generateSuccessor(self.agentIndex, action)
        childIndex = self.agentIndex + 1
        if childIndex == self.numAgents:  # child is a pacman layer
            childNode = MinimaxNode(childState, 0, self.depth + 1, self.maxDepth, self.evalFn)
        else:
            childNode = MinimaxNode(childState, childIndex, self.depth, self.maxDepth, self.evalFn)
        return childNode

    def getChildren(self):
        """
        Returns a list of children nodes of the current node
        :return: list of children
        """
        result = []
        for action in self.gameState.getLegalActions(self.agentIndex):
            childNode = self.generateChildNode(action)
            result.append(childNode)
        return result

    def getChildrenWithAction(self):
        """
        Same with getChildren(), but also returns the actions associates with the children
        :return: list of tuple of (action, childNode)
        """
        result = []
        for action in self.gameState.getLegalActions(self.agentIndex):
            childNode = self.generateChildNode(action)
            result.append((action, childNode))
        return result

    def getScore(self):
        """
        Finds the minimax score of current node. Recursive.
        :return: the score
        """
        if self.depth > self.maxDepth:
            return self.evalFn(self.gameState)
        if self.gameState.isWin():
            return self.evalFn(self.gameState)
        if self.gameState.isLose():
            return self.evalFn(self.gameState)
        scores = []
        for child in self.getChildren():
            scores.append(child.getScore())
        if self.agentIndex == 0:
            return max(scores)
        else:
            return min(scores)

        # Explorative question: Because in situations where death is imminent, minimax finds all termination states
        # which include lose states. And it turns our that the dead state gives it more points when die early.


class AlphaBetaNode(MinimaxNode):
    """
    Node for alpha beta pruning
    """

    def __init__(self, gameState, agentIndex, depth, maxDepth, evalFn):
        MinimaxNode.__init__(self, gameState, agentIndex, depth, maxDepth, evalFn)
        self.alpha = float("-inf")
        self.beta = float("inf")

    def setAlpha(self, value):
        """
        Setter for alpha
        """
        self.alpha = value

    def setBeta(self, value):
        """
        Setter for beta
        """
        self.beta = value

    def atMaxNode(self, action):
        """
        Code to do when at a max node
        :param action: the action that applied on this node
        :return: the score of its child, only to be used by the root
        """
        childNode = self.generateChildNode(action)
        childScore = childNode.getScore()
        if childScore >= self.alpha:
            self.setAlpha(childScore)
        return childScore

    def atMinNode(self, action):
        """
        Code to do when at a min node
        :param action: the action that applied on this node
        :return: the score of its child, pretty much useless
        """
        childNode = self.generateChildNode(action)
        childScore = childNode.getScore()
        if childScore <= self.beta:
            self.setBeta(childScore)
        return childScore

    def bestAction(self):
        """
        Finds the best action of the current node
        :return: the best action
        """
        scoresTuple = (0, float("-inf"))  # (action, score)
        for action in self.gameState.getLegalActions(self.agentIndex):
            childScore = self.atMaxNode(action)
            if scoresTuple[1] < childScore:
                scoresTuple = (action, childScore)
        return scoresTuple[0]

    def generateChildNode(self, action):
        """
        Generate the child node by the action applied
        :param action: the action that parent state applied
        """
        childState = self.gameState.generateSuccessor(self.agentIndex, action)
        childIndex = self.agentIndex + 1
        if childIndex == self.numAgents:  # child is a pacman layer
            childNode = AlphaBetaNode(childState, 0, self.depth + 1, self.maxDepth, self.evalFn)
        else:
            childNode = AlphaBetaNode(childState, childIndex, self.depth, self.maxDepth, self.evalFn)
        childNode.setAlpha(self.alpha)
        childNode.setBeta(self.beta)
        return childNode

    def getScore(self):
        """
        Finds the minimax score of current node. Recursive.
        :return: the score
        """
        if self.depth > self.maxDepth:
            return self.evalFn(self.gameState)
        if self.gameState.isWin():
            return self.evalFn(self.gameState)
        if self.gameState.isLose():
            return self.evalFn(self.gameState)
        if self.agentIndex == 0:  # self is a max node
            for action in self.gameState.getLegalActions(self.agentIndex):
                self.atMaxNode(action)
                if self.alpha >= self.beta:
                    return self.alpha
            return self.alpha
        else:  # self is a min node
            for action in self.gameState.getLegalActions(self.agentIndex):
                self.atMinNode(action)
                if self.alpha >= self.beta:
                    return self.beta
            return self.beta


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        root = AlphaBetaNode(gameState, 0, 1, self.depth, self.evaluationFunction)
        return root.bestAction()


class ExpectimaxNode(MinimaxNode):
    """
    Node for expectimax
    """
    def getScore(self):
        """
        Finds the minimax score of current node. Recursive.
        :return: the score
        """
        if self.depth > self.maxDepth:
            return self.evalFn(self.gameState)
        if self.gameState.isWin():
            return self.evalFn(self.gameState)
        if self.gameState.isLose():
            return self.evalFn(self.gameState)
        scores = []
        for child in self.getChildren():
            scores.append(child.getScore())
        if self.agentIndex == 0:
            return max(scores)
        else:
            return float(sum(scores)) / len(scores)

    def generateChildNode(self, action):
        """
        Generate the child node by the action applied
        :param action: the action that parent state applied
        """
        childState = self.gameState.generateSuccessor(self.agentIndex, action)
        childIndex = self.agentIndex + 1
        if childIndex == self.numAgents:  # child is a pacman layer
            childNode = ExpectimaxNode(childState, 0, self.depth + 1, self.maxDepth, self.evalFn)
        else:
            childNode = ExpectimaxNode(childState, childIndex, self.depth, self.maxDepth, self.evalFn)
        return childNode


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        root = ExpectimaxNode(gameState, 0, 1, self.depth, self.evaluationFunction)
        return root.bestAction()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
