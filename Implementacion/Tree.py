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
       Modela un arbol meditante un data type Nodo.
'''

FORK = u'\u251c'
LAST = u'\u2514'
VERTICAL = u'\u2502'
HORIZONTAL = u'\u2500'
VACIO = u' '

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')
    
class Nodo:
    
    def __init__(self,dato,mas_comun=None):
        self.dato = dato
        self.mas_comun = mas_comun
        self.hijos = {}
    
    def add_hijo(self,subarbol,etiqueta):
        self.hijos.update({etiqueta:subarbol})
        
    def predict(self,test,target):
        if self.hijos:
            valor = test[self.dato]
            if self.hijos.has_key(valor):
                return self.hijos[valor].predict(test,target)
            else: # Tengo un valor nuevo atributo (nunca visto) de los ejemplos de entrenamiento
                return 0 if self.mas_comun == test[target] else 1
        else:
            return 0 if self.dato == test[target] else 1
    
    def __str__(self):
        def explore(self, prefijo='',nodos=0):        
            hijos = self.hijos.items()
            next_prefijo = u''.join([prefijo,VERTICAL,u'    '])
            ret = u''.join([u'\n',prefijo,self.dato])
            max_prof = 0
            for etiqueta,subarbol in hijos[:-1]:
                ret += u''.join([u'\n',prefijo,FORK,HORIZONTAL,HORIZONTAL,u' (-',etiqueta,u'-)'])
                ret += u''.join([u'\n',prefijo,VERTICAL,u'    ',VERTICAL])
                tree, nodos, prof = explore(subarbol,next_prefijo,nodos)
                if max_prof < prof : max_prof = prof 
                ret += u''.join([tree])
            if hijos:
                etiqueta, subarbol = hijos[-1]
                last_prefijo = u''.join([prefijo,VACIO,u'    '])
                ret += u''.join([u'\n',prefijo,LAST,HORIZONTAL,HORIZONTAL,u' (-',etiqueta,u'-)'])
                ret += u''.join([u'\n',prefijo,VACIO,u'    ',VERTICAL])
                tree, nodos, prof = explore(subarbol,last_prefijo,nodos)
                if max_prof < prof : max_prof = prof
                ret += u''.join([tree])
            else:
                ret += u''.join([u'\n',prefijo])
            return ret,nodos+1,max_prof+1
        
        tree, nodes, depth = explore(self)
        nodes = u"NODOS:\n%i" % nodes
        depth = u"PROFUNDIDAD:\n%i" % depth
        tree  = u"ARBOL:%s" % tree       
        return u'\n'.join([nodes, depth, tree])

# Test
# h1111 = Nodo(u"h1111")
# h1112 = Nodo(u"h1112")
# h1113 = Nodo(u"h1113")
# h1114 = Nodo(u"h1114")
# h111 = Nodo(u"h111")
# h111.add_hijo(h1111, u"tag 1111")
# h111.add_hijo(h1112, u"tag 1112")
# h111.add_hijo(h1113, u"tag 1113")
# h111.add_hijo(h1114, u"tag 1114")
# h112 = Nodo(u"h112")
# h11 = Nodo(u"h11")
# h11.add_hijo(h111, u"tag 111")
# h11.add_hijo(h112, u"tag 112")
# h12 = Nodo(u"h12")
# h21 = Nodo(u"h21")
# h1 = Nodo(u"h1")
# h1.add_hijo(h11,u"tag 11")
# h1.add_hijo(h12,u"tag 12")
# h2 = Nodo(u"h2")
# h2.add_hijo(h21,u"tag 21")
# root = Nodo(u"raiz")
# root.add_hijo(h1,u"tag 1")
# root.add_hijo(h2,u"tag 2")
#     
# print root
