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

            for estado in estado_listas:
                if "E" in estado:
                    c+=1
            if c != len(ltuneles):
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
                if not robot[3]:
                    lista_acciones.append((robot[0], "mover", (5,1))) #En el primer movimiento todos los robots van a (5,1)
                else:
                    movimientos_posibles = ((-1, 0), (1, 0), (0, 1), (0, -1))
                    for mov in movimientos_posibles:
                        posicion = []
                        posicion_robot = robot[3]
                        x = posicion_robot[0] + mov[0]
                        y = posicion_robot[1] + mov[1]
                        posicion.append((x,y))
                        for i_tunel, tunel in enumerate(tuneles):
                            if posicion == tunel[0]: 
                                if robot[1] == "escaneador" and estado_listas[i_tunel] == "L":
                                    lista_acciones.append((robot[0], "mover", posicion)) #Devuelve el robot, la accion y la posicion adonde se mueve
                                elif robot[1] == "soporte": 
                                    lista_acciones.append((robot[0], "mover", posicion)) #Los soportes se mueven por cualquier posicion

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

            ltuneles = list(tuneles)
            lrobots = []
            for robot in robots:
                lrobots.append(list(robot))
            #for lrobot in lrobots:
            #    lrobot[3] = list(lrobot[3])

            robot_hace, accion, donde = action
            
            nuevo_state = []

            if accion == "mover":                                   #Si la acción es mover
                for i_ltunel, ltunel in enumerate(ltuneles):             
                    if ltunel == donde:          
                        estado_listas[i_ltunel] = "E"
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

            devolver_tuneles = tuple(ltuneles)
            devolver_robots = tuple(devolver_robots)

            nuevo_state = (devolver_tuneles, devolver_robots)

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

if __name__ == '__main__':
    
    robots= [("s1", "soporte"), ("e1", "escaneador"), ("e3", "escaneador")]
    tuneles= [(5, 1), (6 , 1), (6, 2)]

    plan = planear_escaneo(tuneles, robots)
    print(plan)