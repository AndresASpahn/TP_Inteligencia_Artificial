from simpleai.search import SearchProblem
from simpleai.search.traditional import astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
from simpleai.search.viewers import WebViewer, BaseViewer

def planear_escaneo(tuneles, robots):

    class MinaProblem(SearchProblem):
        
#       ---------- IS_GOAL ----------

        def is_goal(self, state):
            
            tuneles, robots = state

            c = 0

            for tunel in tuneles:
                if "E" in tunel[1]:
                    c+=1
            if c != len(tuneles):
                return False
            return True

#       ---------- ACTIONS ----------

        def actions(self, state):
            
            tuneles, robots = state

            lista_acciones = []

            #Hay dos acciones posibles
            #"cargar"
            for robot in robots:
                if robot[2] < 1000 and robot[1] == "escaneador": #Pregunta si hay un escaneador con poca bateria
                    for robot2 in robots:
                        if robot2[1] == "soporte" and robot[3] == robot2[3]:    #Busca un soporte que se encuentre en la misma posicion
                            lista_acciones.append((robot2[0], "cargar", robot[0]))

            #"mover"
            for robot in robots:
                if robot[3] == None:
                    lista_acciones.append((robot[0], "mover", (5,1))) #En el primer movimiento todos los robots van a (5,1)
                else:
                    movimientos_posibles = ((-1, 0), (1, 0), (0, 1), (0, -1))
                    for mov in movimientos_posibles:
                        posicion = []
                        x = robot[3][0] + mov[0]
                        y = robot[3][1] + mov[1]
                        posicion.append((x,y))
                        for tunel in tuneles:
                            if posicion == tunel[0]: 
                                if robot[1] == "escaneador" and tunel[2] == "L":
                                    lista_acciones.append((robot[0], "mover", tuple(posicion))) #Devuelve el robot, la accion y la posicion adonde se mueve
                                elif robot[1] == "soporte": 
                                    lista_acciones.append((robot[0], "mover", tuple(posicion))) #Los soportes se mueven por cualquier posicion

            return tuple(lista_acciones)

#       ---------- COST ----------

        def cost(self, state_ini, action, state_fin):
            robot, accion, donde = action
            if accion == "cargar":
                return 5
            return 1 
        
#       ---------- RESULT ----------

        def result(self, state, action):

            tuneles, robots = state

            tuneles = list(tuneles)
            robots = list(robots)

            robot_hace, accion, donde = action
            
            nuevo_state = []

            if accion == "mover":
                for tunel in tuneles:
                    if tunel[0] == donde:
                        tunel[1] = "E"
                for robot in robots:
                    if robot_hace == robot[0]:
                        robot[2] -= 100
                        robot[3] == tuple(donde)
            elif accion == "cargar":
                for robot in robots:
                    if robot[0] == donde:
                        robot[2] = 1000

            nuevo_state = (tuple(tuneles), tuple(robots))

            return nuevo_state

#       ---------- HEURISTICA ----------

        # def heuristic(self, state):
        #     costo_heuristic = 0
        #     #La heuristica corresponde a los nodos que faltan recorrer. (tunel,"L") 
        #     # multiplicado por el tiempo del robot que menos consume(1 minuto).
        #     tuneles, robots = state
        #     for tunel in tuneles:
        #         if lista_tuneles[i_tunel][1] != "E":        
        #             costo_heuristic += 1    
        #     return costo_heuristic

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #((tunel),("L")) lista_tuneles[1] puede contener una "E" en caso de ser escaneado
    # La "L" significa que el tunel no fue escaneado en esta zona y esta libre
    lista_tuneles = []
    for tunel in tuneles:
        lista_tuneles.append((tunel, ["L"]))

    lista_robots = []
    for robot in robots:
        lista_robots.append((robot[0], robot[1], 1000, [])) #("e1", "escaneador", 1000, []) nombre, descripcion, bateria y posicion actual

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    resultado = []

    lista_tuneles = tuple(lista_tuneles)
    lista_robots = tuple(lista_robots)

    INITIAL_STATE = (lista_tuneles, lista_robots)
    problema = MinaProblem(INITIAL_STATE)
    
    proceso = astar(problema, graph_search=True)

    for action, state in proceso.path():
        if (action is not None):
            resultado.append(action)

    return resultado



# if __name__ == '__main__':

#     robots= [("s1", "soporte"), ("e1", "escaneador"), ("e3", "escaneador")]
#     tuneles= [(5, 1), (6 , 1), (6, 2)]

#     plan = planear_escaneo(tuneles, robots)


#De esta manera agrego dos robots en el mismo lugar
#lista_tuneles[i_tunel][1].append("O")