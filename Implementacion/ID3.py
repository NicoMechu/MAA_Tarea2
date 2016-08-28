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
    Notaciones
    - ejemplos : {(d1,pol1),...,(dM,polM)}, donde d:Dato y pol:Polaridad
    - ejemplo  : {a1:v1,...,aN:vN}, donde a:Atributo y v:Valor
    - polaridad: "+" o "-"
'''

from Tree import Nodo
from math import log
from itertools import groupby
from collections import defaultdict

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
        @param ejemplos: [({d11:v11,...,d1N:v1N},p1),...,({dM1:vM1,...,dMN:vMN},pM)]
        '''

        # Si dan ejemplos nuevos, instanciarlos
        if ejemplos: self.examples = ejemplos

        # Extraer los valores de atributos para cada dato
        for ejemplo in self.examples:
            for atributo, valor in ejemplo.items():
                self.values[atributo].add(valor)

    def execute(self,target_attribute,attributes):
        '''
        Modela el algoritmo ID3
        @param target_atrribute: d:v
        @param atrributes      : []
        '''
        def mas_comun(self,target_attribute):
        # Determina cual es el valor mas comun para el atributo objetivo
            polaridades = list(self.values[target_attribute])
            return max(set(polaridades), key=polaridades.count)

        # Si todos los ejemplos tiene la misma polaridad, returna nodo con esa polaridad
        if len(set(self.values[target_attribute]))==1:
            return Nodo(self.values[target_attribute][0])

        # Si no hay mas atributos, retorna el mas comun
        if not attributes:
            return Nodo(mas_comun(self,target_attribute))

        # En otro caso
        def mejor_clasifica(atts,tatt):
            def information_gain(A,tA,S):
                def subS(v,S,A):
                    # Calcula subconjunto de S donde el atributo A tiene valor v
                    return [s for s in S if s[A]==v]
                def entropy(S,target_attribute):
                    def subclases(S):
                        ordenado = sorted(S, key=lambda s : s[target_attribute])
                        agrupado = groupby(ordenado, key=lambda s : s[target_attribute])
                        # Obtiene las sublclases de S segun su polaridad
                        return [[y for y in list(x[1])] for x in agrupado]
                    # Calcula la entropia de S a partir de las subclases
                    return sum(-(1.0*len(subclass)/len(S))*log((1.0*len(subclass)/len(S)),2) for subclass in subclases(S))
                # Calcula Information Gain a partir de la entropia y las sublcases
                return entropy(S,tA) - sum(entropy(subS(v,S,A),tA) * len(subS(v,S,A))/len(S) for v in self.values[A])
            # Determina cual es el mejor atributo que clasifica a los ejemplos segun el Information Gain
            return max(atts, key=lambda att : information_gain(att,tatt,self.examples))

        A = mejor_clasifica(attributes,target_attribute)
        raiz = Nodo(A)
        for value in self.values[A]: # Buscar hijos
            ejemplos_v = [dato for dato in self.examples if dato[A]==value]
            if not ejemplos_v:
                hijo = Nodo(mas_comun(target_attribute))
            else:
                attributes.pop(A,None)
                hijo = self.execute(target_attribute, attributes)
            raiz.add_hijo(hijo)

        return raiz

    def run(self):
        self.tree = self.execute()

    def evaluate(self,instancia):
        pass

# Test
learn = ID3()

target_attribute = "JugarTenis"

attributes = {"Cielo":"Lluvia", "Temperatura":"Suave", "Humedad":"Alta"  , "Viento":"Fuerte"}
arbol = learn.execute("JugarTenis", attributes)
print 6
