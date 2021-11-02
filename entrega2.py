from typing import List
from simpleai.search import CspProblem, backtrack
from itertools import combinations


#Variables del problema definidas según funcionalidades solicitadas
variables = ["incrementar_autonomia","terreno_irregulares","cargas_extras","comunicacion_robot"]

consumo_base = 100
baterias_base = 1000

#Se planteo un diccionario ya que con la anterior estructura teniamos un problema de type al igual solution al backtrack(problem)
#Se planteo una estructura de diccionario con tuplas adentro. Un indice por cada mejora.
domains = {
    'incrementar_autonomia':
    [
        ('baterias_chicas',10,5000),
        ('baterias_medianas',10,7500),
        ('baterias_grandes',10,10000),
    ]
    ,'terreno_irregulares':
    [
        ('patas_extras',15,0),
        ('mejores_motores',25,0),
        ('orugas',50,0),
    ]
    ,'cargas_extras':
    [
        ('caja_superior',10,0),
        ('caja_trasera',10,0)
    ]
    ,'comunicacion_robot':
    [
        ('video_llamadas',10,0),
        ('radios',5,0)
    ]
    
}

constraints=[]

def es_adm_uruga(variables,values):
    incrementar_autonomia,terreno = values

    if incrementar_autonomia[0]=="baterias_grandes" and terreno[0] in('orugas'):
        return True
    return False

#Función para controlar la autonomía.
def es_autonomo(variables, values):
    var= values[0]
    #Almaceno la carga total de la bateria.
    carga_t = var[2]
    consumo_T = 0
    consumo_x_minuto = 0

    #Acumulo los costos de cada movimiento extras y además le sumo el base. 
    for x in values:
        consumo_x_minuto += x[1]

    consumo_T= consumo_x_minuto 

    return (carga_t/consumo_T) >= 50

#Controlar la autonomía.

def es_compatible_motor_radio(variables,values):
    #Si la radio esta asociada a una mejora de un motor, devuelvo False ya que no pueden convivir porque no son compatibles.
    terrenos,comunicacion = values
    if ((terrenos[0] == "mejores_motores") and (comunicacion[0] != 'radios')):
        return True
    return False

# Restricción: si usa sistema de videollamadas necesita el par extra de patas o las orugas
def es_compatible_videollamada(variables,values):
    terrenos,comunicacion = values
    if ((comunicacion[0] == "video_llamadas") and (terrenos[0] in('patas_extras','orugas'))):
        return True
    return False    


#constraints.append(((variables),es_autonomo))
constraints.append((('incrementar_autonomia','terreno_irregulares'),es_adm_uruga))   
#constraints.append((('terreno_irregulares', 'comunicacion_robot'), es_compatible_motor_radio))
#constraints.append((('terreno_irregulares', 'comunicacion_robot'), es_compatible_videollamada))

#Función rediseñar.
def rediseñar_robot():
    problem = CspProblem(variables,domains,constraints)
    solution = backtrack(problem)
    lista_soluciones=[]
    #print("Solution:")
    lista_soluciones.append(solution['incrementar_autonomia'][0])
    lista_soluciones.append(solution['terreno_irregulares'][0])
    lista_soluciones.append(solution['cargas_extras'][0])
    lista_soluciones.append(solution['comunicacion_robot'][0])
 
    return lista_soluciones 
    #print(solution['incrementar_autonomia'][0])
# Aca vamos a definir la función para la adaptación
adaptaciones = rediseñar_robot()
print(adaptaciones)