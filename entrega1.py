from simpleai.search import SearchProblem
from simpleai.search import viewers
from simpleai.search.traditional import astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
from simpleai.search.viewers import WebViewer, BaseViewer

def planear_escaneo(tuneles, robots):

    class MinaProblem(SearchProblem):
        
#       ---------- IS_GOAL ----------
        def is_goal(self, state):
            ltuneles, lrobots = state
            if len(ltuneles) == 0:
                return True
            return False

#       ---------- ACTIONS ----------

        def actions(self, state):
            
            ltuneles, lrobots = state

            movimientos_posibles = ((1, 0), (0, 1), (-1, 0), (0, -1))
            lista_acciones = []

            for robot in lrobots:
                if robot[1] == "escaneador"and robot[2] >= 100:
                    for mov in movimientos_posibles:
                        posicion = []
                        posicion_robot = robot[3]
                        posicion.append((posicion_robot[0] + mov[0], posicion_robot[1] + mov[1]))
                        if posicion[0] in tuneles: 
                            lista_acciones.append((robot[0], "mover", tuple(posicion[0]))) #Devuelve el robot, la accion y la posicion adonde se mueve
                else:
                    for robot_sin_carga in lrobots:    
                        if robot_sin_carga[1] == "escaneador" and robot_sin_carga[2] < 100 and robot[3] == robot_sin_carga[3]: #Pregunta si hay un escaneador con poca bateria
                            lista_acciones.append((robot[0], "cargar", robot_sin_carga[0]))
                    for mov in movimientos_posibles:
                        posicion = []
                        posicion_robot = robot[3]
                        x = posicion_robot[0] + mov[0]
                        y = posicion_robot[1] + mov[1]
                        posicion.append((x,y))
                        if posicion[0] in tuneles_completos: 
                            lista_acciones.append((robot[0], "mover", tuple(posicion[0])))

            return lista_acciones

#       ---------- RESULT ----------

        def result(self, state, action):

            ltuneles, lrobots = state
            robot_hace, accion, donde = action

            lrobots = list(list(x) for x in lrobots)
            ltuneles = list(ltuneles)
            energia = 0

            if accion == "mover":
                for indice, robot in enumerate(lrobots):
                    if robot_hace == robot[0]:
                        nuevo_robot = list(robot)
                        lrobots.remove(robot)
                        if nuevo_robot[1] == "escaneador":
                            if donde in ltuneles:
                                ltuneles.remove(donde)
                                energia = nuevo_robot[2] - 100
                                nuevo_robot[2] = energia
                        nuevo_robot[3] = donde
                        lrobots.insert(indice, nuevo_robot)
            elif accion == "cargar":
                for indice, robot in enumerate(lrobots):
                    if robot[0] == donde:
                        robot[2] = 1000
            lrobots = tuple(tuple(x) for x in lrobots)

            nuevo_state = (tuple(ltuneles), lrobots)
            
            return nuevo_state

#       ---------- COST ----------

        def cost(self, state_ini, action, state_fin):
            robot_hace, accion, donde = action
            if accion == "cargar":
                return 5
            return 1 

#       ---------- HEURISTICA ----------

        # def heuristic(self, state):
        #     costo_heuristic = 0
        #     #La heuristica corresponde a los nodos que faltan recorrer. (tunel,"L") 
        #     # multiplicado por el tiempo del robot que menos consume(1 minuto).
        #     tuneles, robots = state
        #     for i_tunel, tunel in enumerate(tuneles):
        #         if estado_listas[i_tunel] != "E":        
        #             costo_heuristic += 1    
        #     return costo_heuristic

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    tuneles_completos = tuple(tuneles)

    lista_robots = []
    for robot in robots:
        lista_robots.append((robot[0], robot[1], 1000, (5,0))) #("e1", "escaneador", 1000, []) nombre, descripcion, bateria y posicion actual

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    resultado = []

    lista_tuneles = tuple(tuneles)
    lista_robots = tuple(lista_robots)

    INITIAL_STATE = (lista_tuneles, lista_robots)
    problema = MinaProblem(INITIAL_STATE)
    
    metodo = astar(problema, graph_search=True)

    for action in metodo.path():
        if action[0] is not None:
            resultado.append(action[0])

    return resultado

if __name__ == '__main__':
    
    E1 = ("e1", "escaneador")
    E2 = ("e2", "escaneador")
    E3 = ("e3", "escaneador")
    S1 = ("s1", "soporte")
    S2 = ("s2", "soporte")

    robots= [E1, S1]

    MINA_TUNEL_RECTO_LARGO = (
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11),)

    plan = planear_escaneo(MINA_TUNEL_RECTO_LARGO, robots)
    print(plan)