from typing import List
from simpleai.search import CspProblem, backtrack
from itertools import combinations


#Variables del problema definidas según funcionalidades solicitadas
variables_problem = ['incrementar_autonomia','terreno_irregulares','cargas_extras','comunicacion_robot']

consumo_base = 100
baterias_base = 1000

#Se planteo un diccionario ya que con la anterior estructura teniamos un problema de type al igual solution al backtrack(problem)
#Se planteo una estructura de diccionario con tuplas adentro. Un indice por cada mejora.
domains = {
    'incrementar_autonomia':
    [
        ('baterias_chicas',10,4000),
        ('baterias_medianas',20,6500),
        ('baterias_grandes',50,9000),
    ]
    ,'terreno_irregulares':
    [
        ('patas_extras',15),
        ('mejores_motores',25),
        ('orugas',50,0),
    ]
    ,'cargas_extras':
    [
        ('caja_superior',10),
        ('caja_trasera',10)
    ]
    ,'comunicacion_robot':
    [
        ('video_llamadas',10),
        ('radios',5)
    ]
    
}

constraints=[]

def es_adm_uruga(variables,values):
    incrementar_autonomia,terreno = values
    has_bateriasgrandes = "baterias_grandes" in incrementar_autonomia[0]
    has_orugas = "mejores_motores" in terreno[0]

    if (has_bateriasgrandes):
        return has_orugas
    else:
        return True

#Función para controlar la autonomía.
def es_autonomo(variables, values):
    var= values[0]
    x=0
    #Almaceno la carga total de la bateria.
    carga_t = var[2]
    consumo_resultante = 0
    consumo_x_minuto = 0
    #Acumulo los costos de cada movimiento extras y además le sumo el base. 
    for x in values:
        consumo_x_minuto += x[1]

    consumo_resultante= consumo_x_minuto + consumo_base
    bateria_resultante = carga_t + baterias_base

    return ((bateria_resultante/consumo_resultante) >= 50)

#Controlar la autonomía.

def es_compatible_motor_radio(variables,values):
    terrenos,comunicacion = values
    #Si hay  mejores motores no puede haber radios.
    has_mejora = "mejores_motores" in terrenos[0]
    has_radio = "radios" in comunicacion[0]
    if has_mejora:
        return not has_radio
    else:
        return True


# Restricción: si usa sistema de videollamadas necesita el par extra de patas o las orugas
def es_compatible_videollamada(variables,values):
    terrenos,comunicacion = values
    comunic = "video_llamadas" in comunicacion[0] 
    terre= terrenos[0] in('patas_extras','orugas')
    if comunic:
        return terre
    else:
        True


 #constraints.append((variables_problem,es_autonomo))
constraints.append((('incrementar_autonomia','terreno_irregulares'),es_adm_uruga))   
constraints.append((('terreno_irregulares', 'comunicacion_robot'), es_compatible_motor_radio))
constraints.append((('terreno_irregulares', 'comunicacion_robot'), es_compatible_videollamada))

#Función rediseñar.
# Aca vamos a definir la función para la adaptación
def rediseñar_robot():
    
    problem = CspProblem(variables_problem,domains,constraints)
    solution = backtrack(problem)
    lista_soluciones=[]
    #print("Solution:")
    lista_soluciones.append(solution['incrementar_autonomia'][0])
    lista_soluciones.append(solution['terreno_irregulares'][0])
    lista_soluciones.append(solution['cargas_extras'][0])
    lista_soluciones.append(solution['comunicacion_robot'][0])

    return lista_soluciones
    
    #print(solution['incrementar_autonomia'][0])

if __name__ == '__main__':
    problem = CspProblem(variables_problem, domains, constraints)
    solution = backtrack(problem)
    adaptaciones = rediseñar_robot()
    print(adaptaciones)