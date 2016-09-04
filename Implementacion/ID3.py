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
   Modela el algoritmo ID3.

@attention: 
    ejemplos  : [{a1:v1,...,aN:vN}], donde a:Atributo y v:Valor  
'''

from Tree import Nodo, FORK, LAST, VERTICAL, HORIZONTAL
from math import log
from itertools import groupby
from collections import defaultdict
from random import sample

class ID3:
    '''
    @summary:    
    ''' 
    # Dataset - Proposito de test. Tomado del libro.
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
    values    = defaultdict(set)
    max_depht = None
    
    def __init__(self,ejemplos=None,max_prof=None):
        '''
        Instancia la clase, indicando opcionalmente un dataset de ejemplos  
        @parm : Conjunto de ejemplos sobre los que se basara el algoritmo
        '''
        # Si dan ejemplos nuevos, instanciarlos
        if ejemplos: self.examples = ejemplos
        
        # Dar limite de profundidad para poda
        if max_prof: self.max_depht = max_prof
        
        # Extraer los valores de atributos para cada dato
        for example in self.examples:
            for atributo, valor in example.items():
                self.values[atributo].add(valor) 
    
    def decision_tree(self, target_attribute):
        '''
        Modela el algoritmo ID3 y devuelve el arbol de decision
        @param target_atrribute : Algun valor presente en el dataset
        '''
        
        def execute(target_attribute, attributes, S=self.examples, depth=0):
            # Computa el algoritmo ID3
            
            def mas_comun(tA,S=self.examples):
                # Determina cual es el valor mas comun para el atributo objetivo
                # para un determinado subconjunto de ejemplos
                polaridades = map(lambda s: s[tA],S) 
                return max(polaridades, key=polaridades.count)
            
            def subS(v,S,A):
                # Calcula subconjunto de S donde el atributo A tiene valor v
                return [s for s in S if s[A] == v]
            
            # Si todos los ejemplos tiene la misma polaridad, returna nodo con esa polaridad
            if len(self.values[target_attribute])==1:
                return Nodo(self.values[target_attribute][0])
            
            # Si no hay mas atributos o alcanza un max, retorna el mas comun
            if not attributes or (self.max_depht and depth > self.max_depht):
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
            raiz = Nodo(A,mas_comun(target_attribute,S))
            for value in self.values[A]: # Buscar hijos
                ejemplos_v = subS(value, S, A)
                if not ejemplos_v:
                    hijo = Nodo(mas_comun(target_attribute))
                else:
                    attributes.remove(A)
                    hijo = execute(target_attribute, attributes, S=ejemplos_v,depth=depth+1)
                    attributes.append(A)
                raiz.add_hijo(hijo,value)                
            
            return raiz
        
        Atts = [A for A in self.examples[0].keys() if A != target_attribute]
        # importa el valor que tiene el t_A?
        return execute(target_attribute,Atts)

# Test
# learn = ID3()
#  
# target_attribute = "JugarTenis"
#   
# arbol = learn.decision_tree(target_attribute)
# print arbol
