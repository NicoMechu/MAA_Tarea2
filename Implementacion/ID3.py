'''
Metodos de Aprendizaje Automatico
Facultad de Ingenieria (UdelaR), 2016
Practico 2, Ejercicio 6

@author: 
    Erguiz, Daniel        4.554.025-3
    Mechulam, Nicolas     4.933.997-7
    Salvia, Damian        4.452.120-0
    
@summary: 
   Modela el algoritmo ID3.
   Realiza su entrenamiento y verificacion.

@attention: 
    ejemplos  : [{a1:v1,...,aN:vN}], donde a:Atributo y v:Valor  
'''

from Tree import Nodo
from math import log
from itertools import groupby
from collections import defaultdict
from copy import deepcopy

class ID3:
    '''
    @summary:    
    ''' 
    # Dataset
    examples = [
            {"Cielo":"Sol"   , "Temperatura":"Alta" , "Humedad":"Alta"  , "Viento":"Debil"  ,"JugarTenis":'-'},
            {"Cielo":"Sol"   , "Temperatura":"Alta" , "Humedad":"Alta"  , "Viento":"Fuerte" ,"JugarTenis":'-'},
            {"Cielo":"Nubes" , "Temperatura":"Alta" , "Humedad":"Alta"  , "Viento":"Debil"  ,"JugarTenis":'+'},
            {"Cielo":"Lluvia", "Temperatura":"Suave", "Humedad":"Alta"  , "Viento":"Debil"  ,"JugarTenis":'+'},
            {"Cielo":"Lluvia", "Temperatura":"Baja" , "Humedad":"Normal", "Viento":"Debil"  ,"JugarTenis":'+'},
            {"Cielo":"Lluvia", "Temperatura":"Baja" , "Humedad":"Normal", "Viento":"Fuerte" ,"JugarTenis":'-'},
            {"Cielo":"Nubes" , "Temperatura":"Baja" , "Humedad":"Normal", "Viento":"Fuerte" ,"JugarTenis":'+'},
            {"Cielo":"Sol"   , "Temperatura":"Suave", "Humedad":"Alta"  , "Viento":"Debil"  ,"JugarTenis":'-'},
            {"Cielo":"Sol"   , "Temperatura":"Baja" , "Humedad":"Normal", "Viento":"Debil"  ,"JugarTenis":'+'},
            {"Cielo":"Lluvia", "Temperatura":"Suave", "Humedad":"Normal", "Viento":"Debil"  ,"JugarTenis":'+'},
            {"Cielo":"Sol"   , "Temperatura":"Suave", "Humedad":"Normal", "Viento":"Fuerte" ,"JugarTenis":'+'},
            {"Cielo":"Nubes" , "Temperatura":"Suave", "Humedad":"Alta"  , "Viento":"Fuerte" ,"JugarTenis":'+'},
            {"Cielo":"Nubes" , "Temperatura":"Alta" , "Humedad":"Normal", "Viento":"Debil"  ,"JugarTenis":'+'},
            {"Cielo":"Lluvia", "Temperatura":"Suave", "Humedad":"Alta"  , "Viento":"Fuerte" ,"JugarTenis":'-'}
        ]
    values   = defaultdict(set)
    ejemplos = []
    
    def __init__(self,ejemplos=None):
        '''
        Instancia la clase, indicando opcionalmente un dataset de ejemplos  
        '''
        
        # Si dan ejemplos nuevos, instanciarlos
        if ejemplos: self.examples = ejemplos
        
        # Extraer los valores de atributos para cada dato
        for example in self.examples:
            for atributo, valor in example.items():
                self.values[atributo].add(valor) 
        
    def execute(self,target_attribute,attributes,S=examples):
        '''
        Modela el algoritmo ID3
        @param target_atrribute: algun valor presente en el dataset
        @param atrributes      : conjunto de atributos a evaluar  
        '''
        def mas_comun(tA,S=self.examples):
            # Determina cual es el valor mas comun para el atributo objetivo
            # para un determinado subconjunto de ejemplos
            polaridades = [v for s in S for A,v in s.items() if A == tA]
            return max(polaridades, key=polaridades.count)
        
        def subS(v,S,A):
            # Calcula subconjunto de S donde el atributo A tiene valor v
            return [s for s in S if s[A] == v]
        
        # Si todos los ejemplos tiene la misma polaridad, returna nodo con esa polaridad
        if len(set(self.values[target_attribute]))==1:
            return Nodo(self.values[target_attribute][0])
        
        # Si no hay mas atributos, retorna el mas comun
        if not attributes:
            return Nodo(mas_comun(target_attribute,S))
        
        # En otro caso
        def mejor_clasifica(As,tA):            
            def information_gain(A,tA,S):
                def entropy(S,tA):                    
                    def subclases(S):
                        ordenado = sorted(S, key=lambda s : s[tA])
                        agrupado = groupby(ordenado, key=lambda s : s[tA])
                        # Obtiene las sublclases de S segun su polaridad
                        return [[y for y in list(x[1])] for x in agrupado]
                    # Calcula la entropia de S a partir de las subclases
                    return sum(-(1.0*len(subclass)/len(S))*log((1.0*len(subclass)/len(S)),2) for subclass in subclases(S))
                # Calcula Information Gain a partir de la entropia y las sublcases
                return entropy(S,tA) - sum(entropy(subS(v,S,A),tA) * len(subS(v,S,A))/len(S) for v in self.values[A])
            # Determina cual es el mejor atributo que clasifica a los ejemplos segun el Information Gain
            return max(As, key=lambda A : information_gain(A,tA,self.examples))
            
        A = mejor_clasifica(attributes,target_attribute)
        raiz = Nodo(A)
        for value in self.values[A]: # Buscar hijos
            ejemplos_v = subS(value, S, A)
            if not ejemplos_v:
                hijo = Nodo(mas_comun(target_attribute))
            else:
                attributes.remove(A)
                hijo = self.execute(target_attribute, attributes, S=ejemplos_v)
                attributes.append(A)
            raiz.add_hijo(hijo,value)                
        
        return raiz
    
    def train(self):
        self.tree = self.execute()
    
    def evaluate(self,instancia):
        pass

# Test
learn = ID3()

target_attribute = "JugarTenis"
attributes = ["Cielo", "Temperatura", "Humedad", "Viento"]

arbol = learn.execute(target_attribute, attributes)
print arbol
