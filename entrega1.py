from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    astar,
    iterative_limited_depth_first
)

from simpleai.search.viewers import WebViewer, BaseViewer

class MinaProblem(SearchProblem):
    def is_goal(self, state):
        return

    def actions(self, state):
        return

    def result(self, state, action):
        return state

    def cost(self, state_ini, action, state_fin):
        return

    def heuristic(self, state):
        return

def planear_escaneo(metodo, camiones, paquetes):
    return