from simpleai.search import SearchProblem
from simpleai.search.traditional import astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
from simpleai.search.viewers import WebViewer, BaseViewer

def planear_escaneo(tuneles, robots):

    class MinaProblem(SearchProblem):
        
#       ---------- IS_GOAL ----------

        def is_goal(self, state):
            
            ltuneles, robots = state

            c = 0

            if estado_listas.count("E") == len(estado_listas):
                return True
            return False

#       ---------- ACTIONS ----------

        def actions(self, state):
            
            tuneles, robots = state

            lista_acciones = []

            #Hay dos acciones posibles
            #"cargar"
            if "soporte" in robots:
                for robot in robots:
                    if robot[2] < 1000 and robot[1] == "escaneador": #Pregunta si hay un escaneador con poca bateria
                        for robot2 in robots:
                            if robot2[1] == "soporte" and robot[3] == robot2[3]:    #Busca un soporte que se encuentre en la misma posicion
                                lista_acciones.append((robot2[0], "cargar", robot[0]))

            #"mover"
            for robot in robots:
                if not robot[3]:
                    posicion = []
                    posicion.append((5,1))
                    lista_acciones.append((robot[0], "mover", tuple(posicion))) #En el primer movimiento todos los robots van a (5,1)
                else:
                    movimientos_posibles = ((-1, 0), (1, 0), (0, 1), (0, -1))
                    for mov in movimientos_posibles:
                        posicion = []
                        posicion_robot = robot[3]
                        x = posicion_robot[0][0] + mov[0]
                        y = posicion_robot[0][1] + mov[1]
                        posicion.append((x,y))
                        if posicion[0] in tuneles:                  #Si es un tunel que debería ser escaneado
                            indice = tuneles.index(posicion[0])     #Saco el indice
                            if robot[1] == "escaneador" and estado_listas[indice] == "L":
                                lista_acciones.append((robot[0], "mover", tuple(posicion))) #Devuelve el robot, la accion y la posicion adonde se mueve
                            elif robot[1] == "soporte": 
                                lista_acciones.append((robot[0], "mover", tuple(posicion))) #Los soportes se mueven por cualquier posicion

            acciones = tuple(lista_acciones)

            return acciones

#       ---------- COST ----------

        def cost(self, state_ini, action, state_fin):
            robot, accion, donde = action
            if accion == "cargar":
                return 5
            return 1 
        
#       ---------- RESULT ----------

        def result(self, state, action):

            tuneles, robots = state

            lrobots = []
            for robot in robots:
                lrobots.append(list(robot))
            #for lrobot in lrobots:
            #    lrobot[3] = list(lrobot[3])

            robot_hace, accion, donde = action
            
            nuevo_state = []

            if accion == "mover":                                   #Si la acción es mover
                if donde[0] in tuneles:                                #Si es un tunel que debería ser escaneado
                    indice = tuneles.index(donde[0])         
                    estado_listas[indice] = "E"
                for robot in lrobots:
                    if robot_hace == robot[0]:
                        robot[3] = list(robot[3])
                        robot[2] -= 100
                        robot[3] = donde
                        #robot[3].clear()
                        #robot[3].append(donde)
            elif accion == "cargar":
                for robot in lrobots:
                    if robot[0] == donde:
                        robot[2] = 1000

            devolver_robots = []

            for robot in lrobots:
                devolver_robots.append(tuple(robot))

            devolver_robots = tuple(devolver_robots)

            nuevo_state = (tuneles, devolver_robots)

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
    estado_listas = []
    for tunel in tuneles:
        estado_listas.append("L")

    lista_robots = []
    for robot in robots:
        lista_robots.append((robot[0], robot[1], 1000, tuple())) #("e1", "escaneador", 1000, []) nombre, descripcion, bateria y posicion actual

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    resultado = []

    lista_tuneles = tuple(tuneles)
    lista_robots = tuple(lista_robots)

    INITIAL_STATE = (lista_tuneles, lista_robots)
    problema = MinaProblem(INITIAL_STATE)
    
    metodo = astar(problema, graph_search=True)

    for action, state in metodo.path():
        if (action is not None):
            resultado.append(action)

    return resultado

# if __name__ == '__main__':
    
#     E1 = ("e1", "escaneador")
#     E2 = ("e2", "escaneador")
#     E3 = ("e3", "escaneador")
#     S1 = ("s1", "soporte")
#     S2 = ("s2", "soporte")

#     robots= [E1]
#     tuneles= [(5, 1), (6 , 1), (6, 2)]

#     MINA_UN_CASILLERO = ((5, 1), )
#     MINA_TUNEL_RECTO = ((5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),)

#     plan = planear_escaneo(MINA_TUNEL_RECTO, robots)
#     print(plan)