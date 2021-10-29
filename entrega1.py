from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import itertools
from simpleai.search.viewers import WebViewer, BaseViewer

def planear_escaneo(tuneles, robots):
    
    #En esta lista va la estructura necesaria para las respuestas del TP
    resultado = []

    #Primero creamos lista con estados de los tuneles (L=Libre, "s1"=se encuentra un robot en el, E=Escaneado)
    lista_tuneles = []

    #Todos los tuneles quedan como libres
    for i_tunel, tunel in enumerate(tuneles):
        lista_tuneles.append((tunel, ["L"]))

        #De esta manera agrego dos robots en el mismo lugar
        #lista_tuneles[i_tunel][1].append("O")


    #Ahora le asignamos la batería restante y el camino que recorrio (para poder cargarlo) a los robots
    lista_robots = []
    for i_robot, robot in enumerate(robots):
        if robot[1] == "escaneador":
            lista_robots.append((robot[0], 1000, []))

    class MinaProblem(SearchProblem):
        def is_goal(self, state):
            #Es True si todas las posiciones se recorrieron
            #Se necesita tener el recorrido en algún lado
            for i_tunel, tunel in enumerate(lista_tuneles):
                if lista_tuneles[i_tunel][1] != "E":        
                    return False
            return True

        def actions(self, state):
            lista_acciones = []
            tuneles, robots = state
            #Hay dos acciones posibles
            #"mover"
            movimientos_posibles = ((-1, 0), (1, 0), (0, -1), (0, 1))
            for tunel in tuneles:
                for mov in movimientos_posibles:
                    posicion = []
                    x=tunel[0]+mov[0]
                    y=tunel[1]+mov[1]
                    posicion.append((x,y))
                    if posicion[0] in tuneles :
                        for tunel in lista_tuneles:
                            if tunel[0] == posicion[0] and tunel[1] == "L":
                                lista_acciones.append(("mover", posicion[0]))
            #"cargar"
            for robot in lista_robots:
                if robot[1] < 1000:
                    lista_acciones.append(("cargar", robot[0]))

            return lista_acciones

        def cost(self, state_ini, action, state_fin):
            accion, posicion = action
            if accion == "cargar":
                return 5
            return 1 
        
        def result(self, state, action):
            #Estado (Tuneles + Robots)
            tuneles, robots = state
            #Acciones 
            accion, posicion = action

            return state

        def heuristic(self, state):
            costo_heuristic = 0
            #La heuristica corresponde a los nodos que faltan recorrer. (tunel,"L") 
            # multiplicado por el tiempo del robot que menos consume(1 minuto).
            tuneles, robots = state
            for tunel in tuneles:
                if lista_tuneles[i_tunel][1] != "E":        
                    costo_heuristic += 1    
            return costo_heuristic
            
    INITIAL_STATE = (tuple(tuneles), tuple(robots))
    problema = MinaProblem(INITIAL_STATE)

    return resultado

if __name__ == '__main__':

    robots= [("s1", "soporte"), ("e1", "escaneador"), ("e3", "escaneador")]
    tuneles= [(5, 1), (6 , 1), (6, 2)]

    plan = planear_escaneo(tuneles, robots)