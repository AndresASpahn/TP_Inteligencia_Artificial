from simpleai.search import (CspProblem, backtrack)
from itertools import combinations


#Variables del problema definidas según funcionalidades solicitadas
problem_variables = ["incrementar_autonomia","terreno_irregulares","cargas_extras","comunicacion_robot"]
domains ={}

#Dominio correspondiente al incremento de autonomia local
# (Desc),(nuevaCarga),(Costo movimiento extra)

domains[problem_variables[0]] =[
    (("baterias_chicas"),(500),(10)),
    (("baterias_medianas"),(7500),(20)),
    (("baterias_grandes"),(10000),(50))]

#Adaptación Terrenos irregulares
#(nombre,costo_extra)

domains[problem_variables[1]] =[
    (("patas_extras"),(15)),
    (("mejores_motores"),(25)),
    (("orugas"),(50))]

#Suministros 
#(descripcion),(consumoxmovimiento)
domains[problem_variables[2]] =[
    (("caja_superior"),(10)),
    (("caja_trasera"),(10)),]

#Comunicación con robot 
#(nombre),(costo_consumo por movimiento)
domains[problem_variables[3]] =[
    (("videollamada"),(10)),(("radio"),(5))]

#print (domains[problem_variables[0]]) 
#print (domains[problem_variables[1]])    
#print (domains[problem_variables[2]]) 
#print (domains[problem_variables[3]]) 

constraints= []

# Aca vamos a definir la función para la adaptación
def rediseñar_robot():
    problema = CspProblem(problem_variables, domains, constraints)
    solucion = backtrack(problema) 
    solucion = list(solucion.values())

    lista_adaptaciones = []
    for adaptacion in solucion:
        lista_adaptaciones.append(adaptacion[0])
    return lista_adaptaciones
    
if __name__ == '__main__':
    
    import os
    import sys

    print(os.path.dirname(sys.executable))  
    prueba = rediseñar_robot()
    print(prueba)
