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
    
class Nodo:
    
    def __init__(self, dato):
        self.dato = dato
        self.hijos = {}
    
    def add_hijo(self,subarbol,etiqueta):
        self.hijos.update({etiqueta:subarbol})

    def __unicode__(self, prefijo=''):        
        hijos = self.hijos.items()
        next_prefijo = u''.join([prefijo,VERTICAL,u'    '])
        ret = u''.join([u'\n',prefijo,self.dato])
        for etiqueta,subarbol in hijos[:-1]:
            ret += u''.join([u'\n',prefijo,FORK,HORIZONTAL,HORIZONTAL,u' (-',etiqueta,u'-)'])
            ret += u''.join([u'\n',prefijo,VERTICAL,u'    ',VERTICAL]) 
            ret += u''.join([subarbol.__unicode__(next_prefijo)])
        if hijos:
            etiqueta, subarbol = hijos[-1]
            last_prefijo = u''.join([prefijo,VACIO,u'    '])
            ret += u''.join([u'\n',prefijo,LAST,HORIZONTAL,HORIZONTAL,u' (-',etiqueta,u'-)'])
            ret += u''.join([u'\n',prefijo,VACIO,u'    ',VERTICAL])
            ret += u''.join([subarbol.__unicode__(last_prefijo)])
        else:
            ret += u''.join([u'\n',prefijo])
        return ret
    
    def __str__(self):
        return self.__unicode__().encode("utf-8")

# Test
# h1111 = Nodo(u"h1111")
# h1112 = Nodo(u"h1112")
# h1113 = Nodo(u"h1113")
# h111 = Nodo(u"h111")
# h111.add_hijo(h1111, u"soy 1111")
# h111.add_hijo(h1112, u"soy 1112")
# h111.add_hijo(h1113, u"soy 1113")
# h11 = Nodo(u"h111")
# h11.add_hijo(h111, u"soy 111")
# h12 = Nodo(u"h12")
# h21 = Nodo(u"h21")
# h1 = Nodo(u"h1")
# h1.add_hijo(h11,u"soy 11")
# h1.add_hijo(h12,u"soy 12")
# h2 = Nodo(u"h2")
# h2.add_hijo(h21,u"soy 21")
# root = Nodo(u"raiz")
# root.add_hijo(h1,u"soy 1")
# root.add_hijo(h2,u"soy 2")
#  
# print root
