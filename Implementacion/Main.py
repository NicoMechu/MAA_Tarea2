# -*- coding: utf-8 -*-
'''
Metodos de Aprendizaje Automatico
Facultad de Ingenieria (UdelaR), 2016
Practico 2, Ejercicio 6

@author: 
    Erguiz, Daniel        4.554.025-3
    Mechulam, Nicolas     4.933.997-7
    Salvia, Damian        4.452.120-0
    
@summary: 
       Obtiene los datos del dataset y los procesa
       a fin de obtener el arbol de desicion
'''

from ID3 import ID3
from Tree import FORK, LAST, VERTICAL, HORIZONTAL
from csv import DictReader
from random import shuffle

def data(csv_file):
    # Obtiene los ejemplos a partir de un archivo *.csv
    with open(csv_file, mode='r') as f:
        return [row for row in DictReader(f,delimiter=";")]
    
def test(S,slice=0.2,K=10):
    '''
    Ejecuta cross-validation para entrenar y posteriormente evaluar resultados
    a partir de los ejemplos indicados al inicializar
    @param S     : Algun valor presente en el dataset
    @param slice : Porcion de S reservada para test
    @param K     : Tamanio usado en K-fold cross-validation    
    '''
    def KFold(S,K):
        # Pariciona el conjunto S en K parejas (train,test)
        for k in xrange(K):
            train = [x for i,x in enumerate(S) if i % K != k]
            test  = [x for i,x in enumerate(S) if i % K == k]
            yield train, test
            
    # Desordenar muestra S de ejemplos para 
    # separarlo en test y train aleatoriamente
    shuffle(S)
    
    # Particionar la muestra en para entrenamiento y verificacion
    test_size = int(round(len(S)*slice))
    test_sample,train_sample = S[:test_size], S[test_size:]
    print "Total =",len(S),", Test =",len(test_sample),", Train =",len(train_sample)
    
    # Entrenar - Cross-validation de tamanio 10
    best_ID3, best_rate = None, 0.0
    for train, test in KFold(train_sample,K): 
        current_ID3 = ID3(train) # Cargar ejemplos de entrenamiento
        ''' TODO Esta seccion a cotninuacion es similar a la siguiente, unificar? '''
        for example in test: # Probar con cada ejemplo de test
            hits = 0.0 # TODO - Essto esta mal aca, hay que pensar bien donde va
            for tA, tV in example.items(): # Probar con cada atributo como target
                # Extraer el resto de los atributos
                tmp = example.copy() ; tmp.pop(tA)
                As = tmp.keys()
                # Ejecutar algoritmo
                retV = current_ID3.execute(tA,As) # TODO - Esto no devuelve un valor, devuelve un arbol
                # Determinar hit
                if retV == tV: hits += 1
            # Determinar si cambia el mejor
            if best_rate < hits/len(test): 
                best_ID3 = current_ID3
        
    # Verificar
    hits = 0.0
    for test in test_sample:
        for example in test:
            for tA, tV in example.items():
                As = example.copy().pop(tA).keys() 
                retV = best_ID3.execute(tA,As)
                if retV == tV: hits += 1
    print "Accuracy:",hits/len(test_sample)
    
# Primer dataset
dataset1 = data('Dataset/student-mat.csv')
print "Dataset1:",dataset1
learn1 = ID3(dataset1)
test(dataset1) # Total = 395 , Test = 79 , Train = 316

raw_input()

# Segundo dataset
dataset2 = data('Dataset/student-por.csv')
print "Dataset2:",dataset2
learn2 = ID3(dataset2)
test(dataset2) # Total = 649 , Test = 130 , Train = 519

