# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from cmath import inf
from itertools import accumulate
from queue import PriorityQueue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Please DO NOT change the following code, we will use it later
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, '',0, [])
    myPQ.push(startNode,heuristic(startState,problem))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, action, cost, path = node
        if (not state in visited) or cost < best_g.get(state):
            visited.add(state)
            best_g[state]=cost
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                myPQ.push(newNode,heuristic(succState,problem)+cost+succCost)
    util.raiseNotDefined()


def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """

    baseline_coord = problem.getStartState()
    paths = []

    while True:
        queue = util.Queue()
        closed = []
        baseline_h = heuristic(baseline_coord, problem)
        queue.push((baseline_coord, paths, baseline_h))
        while not queue.isEmpty():
            cur_coord, paths, h = queue.pop()
            if cur_coord not in closed:
                closed.append(cur_coord)
                if heuristic(cur_coord, problem) < baseline_h:
                    if problem.isGoalState(cur_coord):
                        return paths
                    baseline_coord = cur_coord
                    break
                for next_coord, action, cost in problem.getSuccessors(cur_coord):
                    queue.push((next_coord, paths+[action], heuristic(next_coord, problem)))
    util.raiseNotDefined()



def bidirectionalAStarEnhanced(problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    """
    Global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call them.
    You need two arguments to call, such as heuristic(state,problem)
    The heuristic functions are "manhattanHeuristic" and "backwardsManhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second (heuristic) and third (heuristic) arguments.
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"

    forwardsPQ = util.PriorityQueue()
    backwardsPQ = util.PriorityQueue()
    start_state = problem.getStartState()
    end_states = problem.getGoalStates()

    for end_state in end_states:
        endNode = (end_state,'',0,[])
        backwardsPQ.update(endNode,backwardsHeuristic(end_state,problem)- heuristic(end_state,problem))

    startNode = (start_state,'',0,[])

    forwardsPQ.update(startNode,heuristic(start_state,problem)- backwardsHeuristic(start_state,problem))

    l=0
    u=inf

    myPQs = [forwardsPQ,backwardsPQ]

    # forwardsPQ.push("1",1)
    # forwardsPQ.push("3",3)
    # forwardsPQ.push("2",2)
    # print(forwardsPQ.getMinimumPriority())
    forwardsClosed = set()
    backwardsClosed = set()

    myCloseds = [forwardsClosed, backwardsClosed]
    direction = 0
    plan = [[],[]]
    node_expansion = []
    while not forwardsPQ.isEmpty() and not backwardsPQ.isEmpty():
        min_f = forwardsPQ.getMinimumPriority()
        min_p = backwardsPQ.getMinimumPriority()
        l = (min_f+min_p)*0.5
        node = myPQs[direction].pop()
        state,action,gn,path = node


        myCloseds[direction].add(state)
        # print(myPQs[0].heap,myPQs[1].heap)
        myheap =  myPQs[abs(direction-1)].heap
        flag = False
        n_gn = 0
        paths=[[],[]]
        paths[direction]=path

        for (p,c,i) in myheap:
            if i[0] == state:
                flag= True
                n_gn = i[2]
                paths[abs(direction-1)] = i[3]
                break


        if flag and n_gn+gn<u:
            u = gn+n_gn
            plans = paths

        node_expansion.append((state,l,u))
        if l>=u:

            forwards_actions = [item[1] for item in plans[0]]
            backwards_actions = [item[1] for item in plans[1]]
            # del forwards_actions[0]
            # del backwards_actions[0]
            backwards_actions.reverse()
            plan = forwards_actions + backwards_actions
            # print(node_expansion)
            print(plan)
            return plan
        succs = []
        if not direction:
            succs = problem.getSuccessors(state)
            for (next_state, next_action, cost) in succs:
                if next_state not in myCloseds[direction]:
                    p= cost+gn + heuristic(next_state,problem)+ cost +gn - backwardsHeuristic(next_state,problem)
                    next_node = (next_state,next_action, gn+cost, path+[(next_state,next_action)])
                    myPQs[direction].update(next_node,p)
        else:
            succs = problem.getBackwardsSuccessors(state)
            for (next_state, next_action, cost) in succs:
                if next_state not in myCloseds[direction]:
                    p= cost+gn + backwardsHeuristic(next_state,problem)+ cost +gn - heuristic(next_state,problem)
                    next_node = (next_state,next_action, gn+cost, path+[(next_state,next_action)])
                    myPQs[direction].update(next_node,p)
        direction = abs(direction -1)



        

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


ehc = enforcedHillClimbing
bae = bidirectionalAStarEnhanced
bae1=bidirectionalAStarEnhanced1
