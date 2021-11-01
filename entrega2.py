from simpleai.search import (CspProblem, backtrack)
from itertools import combinations


#Variables del problema definidas según funcionalidades solicitadas
problem_variables = ["incrementar_autonomia","terreno_irregulares","cargas_extras","comunicacion_robot"]
domains ={}

#Dominio correspondiente al incremento de autonomia local
# (Desc),(nuevaCarga),(Costo movimiento extra)

domains[problem_variables[0]] =[
    ("bateria_chica"),(500),(10),
    ("bateria_mediana"),(7500),(20),
    ("bateria_grande"),(10000),(50)]

#Adaptación Terrenos irregulares
#(nombre,costo_extra)

domains[problem_variables[1]] =[
    (("patas_extras"),(15)),
    (("mot_potente"),(25)),
    (("orugas"),(50))]

#Suministros 
#(descripcion),(consumoxmovimiento)
domains[problem_variables[2]] =[
    (("suministro_hum_tras"),(10)),
    (("suministro_hum_sup"),(10)),]

#Comunicación con robot 
#(nombre),(costo_consumo por movimiento)
domains[problem_variables[3]] =[
    (("videollamada"),(10),)]

#print (domains[problem_variables[0]]) 
#print (domains[problem_variables[1]])    
#print (domains[problem_variables[2]]) 
#print (domains[problem_variables[3]]) 


constraints= []

# Aca vamos a definir la función para la adaptación
def rediseñar_robot():
    problem = CspProblem(problem_variables, domains, constraints)
    pass

