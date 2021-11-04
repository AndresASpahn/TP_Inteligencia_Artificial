from typing import List
from simpleai.search import CspProblem, backtrack
from itertools import combinations


#Variables del problema definidas según funcionalidades solicitadas
variables_problem = ['incrementar_autonomia','terreno_irregulares','cargas_extras','comunicacion_robot']

consumo_base = 100
baterias_base = 1000

#Se planteo un diccionario ya que con la anterior estructura teniamos un problema de type al igual solution al backtrack(problem)
#Se planteo una estructura de diccionario con tuplas adentro.

domains = {
    'incrementar_autonomia':
    [
        #desc,consumo,tamañobateria
        ('baterias_chicas',10,4000),
        ('baterias_medianas',20,6500),
        ('baterias_grandes',50,9000),
    ]
    ,'terreno_irregulares':
    [
        #desc,consumo
        ('patas_extras',15),
        ('mejores_motores',25),
        ('orugas',50),
    ]
    ,'cargas_extras':
    [
        ('caja_superior',10),
        ('caja_trasera',15)
    ]
    ,'comunicacion_robot':
    [
        ('video_llamadas',10),
        ('radios',5)
    ]
    
}

constraints=[]

#Las baterias  grandes solo se utilizan si tiene las orugas
def es_adm_uruga(variables,values):
    incrementar_autonomia,terreno = values

    #Asigno una variable boolean para comprobar existencia de las baterias grandes
    has_bateriasgrandes = 'baterias_grandes' in incrementar_autonomia[0]

    #Asigno una variable boolean para comprobar existencia de las orugas
    has_orugas = 'orugas' in terreno[0]

    if (has_bateriasgrandes):
    
        #Si la bateria es grande, retornamos True en caso que este la oruga, caso que no False.
        return has_orugas
    else:
        #Si no es bateria grande, no tenemos porque restringir, devolvemos True
        return True


#Radio no es compatible con motores potentes.
def es_compatible_motor_radio(variables,values):
    terrenos,comunicacion = values
    has_mejora = 'mejores_motores' in terrenos[0]
    has_radio = 'radios' in comunicacion[0]
    if has_radio:
        return not has_mejora
    else:
        return True

# Restricción: si usa sistema de videollamadas necesita el par extra de patas o las orugas
def es_compatible_videollamada(variables,values):
    terrenos,comunicacion = values

    comunic = 'video_llamadas' in comunicacion[0] 
    terre= terrenos[0] in('patas_extras','orugas')
    if comunic:
        return terre
    else:
        return True
        

#La caja de suminostros Humanitarios en la parte trasera, 
# por su ubicación no es compatible con el par extra de patas, que se ubican en la misma región del chasis.

def es_compatible_patas_suminostrostras(variables,values):
    terreneros,cargas = values
    has_patas = 'patas_extras' in terreneros[0]
    has_chasis = 'caja_trasera' in cargas[0]
    if has_chasis:
        return  not (has_patas)
    return True

#Controlar la autonomia
def es_autonomo(variables,values):
    var= values[0]
    consumos_extras = 0
    bateria = var[2]
    
    for x in values:
        consumos_extras += x[1]
  
    consumo_t = consumo_base + consumos_extras 
    bateria_resultante = baterias_base + bateria

    autonomia = ((bateria_resultante/consumo_t) >= 50)
    return(autonomia)


constraints.append((('terreno_irregulares','cargas_extras'),es_compatible_patas_suminostrostras)) 
constraints.append((('incrementar_autonomia','terreno_irregulares'),es_adm_uruga))   
constraints.append((('terreno_irregulares', 'comunicacion_robot'),es_compatible_motor_radio))
constraints.append((('terreno_irregulares', 'comunicacion_robot'),es_compatible_videollamada))
constraints.append(((variables_problem),es_autonomo))

#Función adaptacion
def rediseñar_robot():
    
    problem = CspProblem(variables_problem,domains,constraints)
    solution = backtrack(problem)
    lista_soluciones=[]

    lista_soluciones.append(solution['incrementar_autonomia'][0])
    lista_soluciones.append(solution['terreno_irregulares'][0])
    lista_soluciones.append(solution['cargas_extras'][0])
    lista_soluciones.append(solution['comunicacion_robot'][0])

    return lista_soluciones
    
if __name__ == '__main__':
    adaptaciones = rediseñar_robot()
    print(adaptaciones)