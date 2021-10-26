from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import itertools

from simpleai.search.viewers import WebViewer, BaseViewer

class MinaProblem(SearchProblem):
    def is_goal(self, state):
        return

    def actions(self, state):
        acciones = []
        a, a = state
        return

    def result(self, state, action):
        return state

    def cost(self, state_ini, action, state_fin):
        return

    def heuristic(self, state):
        return

def planear_escaneo(tuneles, robots):
    return