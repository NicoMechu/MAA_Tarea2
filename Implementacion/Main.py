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
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

def data(csv_file,boolean,without):
    # Obtiene los ejemplos a partir de un archivo *.csv
    with open(csv_file, mode='r') as f:
        D = [row for row in DictReader(f,delimiter=";")]
        # Procesamiento segun las flags
        if boolean: # Transformar a booleano - Update no retorna valores, por eso no se asigna a nada
            [d.update({'G3':('Malo' if int(d['G3']) < 12 else 'Bueno')}) for d in D]
        if without: # Remover G1 y G2
            D = [{k:v for k,v in d.items() if k!='G1' and k!='G2' } for d in D]
        return D 
        
def delta(train_set,test_set,tA):    
    # Calcula el error del algoritmo
    hypotesis = ID3(train_set).decision_tree(tA)
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
        print "\r[CROSS-VALIDATION] Progress: %i/%i" % (cont,TOTAL),
        current_delta = delta(train,test,tA)
        deltas.append(current_delta)
        cont += 1
    
    estimated = sum(deltas)/len(cv_set)
    variance = 1.0*sum([(d - estimated )**2 for d in deltas])/len(cv_set)
    return estimated, variance
    
def process(D,tA,slice=0.2,K=10):
    # Procesa un conjunto de datos D a partir de un atributo objetivo tA
    # particionando la muestra ara entrenamiento y verificacion
    # a fin de evaluar la calidad de la solucion
    shuffle(D)  
    
    test_size = int(round(len(D)*slice))
    test_sample, train_sample = D[:test_size], D[test_size:]
    print "\n[DATOS] Total =",len(D),", Test =",len(test_sample),", Train =",len(train_sample)
    
    delta_estimated, variance = cross_validation(train_sample,tA,K)
    delta_real                = delta(train_sample,test_sample,tA)
    
    return delta_estimated, variance, delta_real

def subcase(dataset,tA):
    d_est, var, d_real = process(dataset,tA)
    res = u"Delta_Estimado = %f , Varianza = %5.3f , Delta_Real = %f" % (d_est,var,d_real)
    tree = ID3(dataset).decision_tree(tA)
    return res, tree.__str__()
    

#########################    PRINCIPAL    ##############################
tA = "G3"
cases = {"MAT":"Dataset/student-mat.csv","POR":"Dataset/student-por.csv"}
# cases = {"TEST":"Dataset/student-test.csv"}
texts  = []

for case,path in cases.items():
    for boolean in ["ENUM","BOOL"]:
        for without in ["CON","SIN"]:
            tcase = "* %s %s %s G1 & G2" % (case, boolean, without)
            print tcase
            dataset = data(path,boolean=="BOOL",without=="SIN")
            res, tree = subcase(dataset,tA)
            texts += [tcase , res] # OBS - Se puede aniadir item 'tree' para dibujar arbol (grande)
            print "\n",tcase,"\n",res

with open('Test.txt','w') as f:
    f.write(u'\n'.join(texts).encode('utf8'))
    