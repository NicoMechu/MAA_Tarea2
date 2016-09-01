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
        
def delta(train_set,test_set,tA):    
    # Calcula el error del algoritmo
    print "Generando arbol de desicion..."
    hypotesis = ID3(train_set).decision_tree(tA)
    print "Evaluando hipotesis..."
    return 1.0*sum(hypotesis.predict(test,tA) for test in test_set)/len(test_set)
    
def cross_validation(S,tA,K):
    '''
    '''
    def KFold(S,K):
        # Pariciona el conjunto S en K parejas (train,test)
        ret = []
        for k in xrange(K):
            train = [x for i,x in enumerate(S) if i % K != k]
            test  = [x for i,x in enumerate(S) if i % K == k]
            ret.append((train,test))
        return ret
        
    # Entrenar - Cross-validation de tamanio 10
    deltas = []
    cv_set = KFold(S,K) 
    TOTAL, cont = len(cv_set), 1
    for train, test in cv_set:
        print "\r [CROSS-VALIDATION] Progreso: %i/%i" % (cont,TOTAL),
        current_delta = delta(train,test,tA)
        deltas.append(current_delta)
        cont += 1
    return sum(deltas)/len(cv_set)
    
def test(D,tA,slice=0.2,K=10):
    # Desordenar muestra S de ejemplos para 
    # separarlo en test y train aleatoriamente
    shuffle(D)
    
    # Particionar la muestra en para entrenamiento y verificacion
    test_size = int(round(len(D)*slice))
    test_sample, train_sample = D[:test_size], D[test_size:]
    print "Total =",len(D),", Test =",len(test_sample),", Train =",len(train_sample)
    
    delta_estimated = cross_validation(train_sample,tA,K)
    delta_real      = delta(train_sample,test_sample,tA)
    
    return delta_estimated, delta_real
    

# Test dataset
dataset = data('Dataset/student-test.csv')
d_est, d_real = test(dataset,"G3")
print "[TEST] Estimado = %f , Real = %f" % (d_est, d_real)
    
# Primer dataset
dataset1 = data('Dataset/student-mat.csv')
d_est, d_real = test(dataset1,"G3")
print "[TEST] Estimado = %f , Real = %f" % (d_est, d_real)

# Segundo dataset
dataset2 = data('Dataset/student-por.csv')
d_est, d_real = test(dataset2,"G3")
print "[TEST] Estimado = %f , Real = %f" % (d_est, d_real)