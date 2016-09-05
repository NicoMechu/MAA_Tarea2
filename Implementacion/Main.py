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
from csv import DictReader
from random import shuffle
import os

max_depth = None

def data(csv_file,boolean,without):
    # Obtiene los ejemplos a partir de un archivo *.csv
    with open(csv_file, mode='r') as f:
        D = [row for row in DictReader(f,delimiter=";")]
        # Procesamiento segun las flags
        if boolean: # Transformar a booleano - Update no retorna valores, por eso no se asigna a nada
            [d.update({'absences':('Aceptable' if int(d['absences']) < 10 else 'Muchas')}) for d in D]
            [d.update({'G1':('Malo' if int(d['G1']) < 12 else 'Bueno')}) for d in D]
            [d.update({'G2':('Malo' if int(d['G2']) < 12 else 'Bueno')}) for d in D]
            [d.update({'G3':('Malo' if int(d['G3']) < 12 else 'Bueno')}) for d in D]
            [d.update({'age':('Menor' if int(d['age']) < 18 else 'Adulto')}) for d in D]
        if without: # Remover G1 y G2
            D = [{k:v for k,v in d.items() if k!='G1' and k!='G2' } for d in D]
        return D 
        
def delta(train_set,test_set,tA):    
    # Calcula el error del algoritmo
    hypotesis = ID3(ejemplos=train_set,max_prof=max_depth).decision_tree(tA)
    return 1.0*sum(hypotesis.predict(test,tA) for test in test_set)/len(test_set)
    
def cross_validation(S,tA,K):
    # Realiza KFold cross-validation de tamanio K sobre el conjunto S
    # a fin de obtener el delta estimado y la varianza
    
    def KFold(S,K):
        # Pariciona el conjunto S en K parejas (train,test)
        for k in xrange(K):
            train = [x for i,x in enumerate(S) if i % K != k]
            test  = [x for i,x in enumerate(S) if i % K == k]
            yield train, test
        
    # Entrenar - Cross-validation de tamanio 10
    deltas, cont = [], 1
    for train, test in KFold(S,K):
        print "\r[CROSS-VALIDATION] Progress: %i/%i" % (cont,K),
        current_delta = delta(train,test,tA)
        deltas.append(current_delta)
        cont += 1
    
    estimated = sum(deltas)/K
    variance = 1.0*sum([(d - estimated )**2 for d in deltas])/K
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

#########################    PRINCIPAL    ##############################
tA = "G3"   
cases = {"MAT":"Dataset/student-mat.csv","POR":"Dataset/student-por.csv"}
# cases = {"TEST":"Dataset/student-test.csv"}
boolean_set = ["ORIG","BOOL"]
without_set = ["CON","SIN"]
max_depths  = [5] # Se pueden agregar mas valores si se desea probar - None:Sin profundidad
 
texts = []
for case,path in cases.items():
    for boolean in boolean_set:
        for without in without_set:
            for max_depth in max_depths:
                tcase = "%s %s %s G1&G2 PROF%s" % (case, boolean, without,str(max_depth))
                print tcase
                dataset = data(path,boolean=="BOOL",without=="SIN")
                d_est, var, d_real = process(dataset,tA)
                res = "\nDELTA_ESTIMADO: %f VARIANZA: %5.3f DELTA_REAL: %f" % (d_est,var,d_real)
                texts += [tcase , res.replace(" ","\n")]
                print res,"\n"
                
                path_res = ''.join(["./Resultados/",'_'.join(tcase.split(' ')),".txt"])
                if not os.path.isdir('./Resultados/'): os.mkdir(os.path.dirname('./Resultados/'))
                print "Copiadondo resultado completo en ",path_res, "..."
                with open(path_res,'w') as f: 
                    tcase = ' '.join(["*",tcase,"*"])
                    f.write('\n'.join([tcase , res.replace(" ","\n"),'\n']))
                    f.write(ID3(ejemplos=dataset,max_prof=max_depth).decision_tree(tA).__str__())
              
with open('Summarize.txt','w') as f:
    f.write('\n'.join(texts))
print "Fin" 
