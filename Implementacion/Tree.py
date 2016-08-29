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

class Nodo:
    
    def __init__(self, dato):
        self.dato = dato
        self.hijos = {}
    
    def add_hijo(self,subarbol,etiqueta):
        self.hijos.update({etiqueta:subarbol})

    def __str__(self,prof=0, prefix=''):        
#         next_prefix = u''.join([prefix, VERTICAL, u'   '])
#         ret = u''
#         for hijo in self.hijos.items()[:-1]:
#             ret += u''.join([prefix, FORK, HORIZONTAL, HORIZONTAL, u' ', hijo[0] ])
#             for resultado in hijo[1].__str__(prof+1,next_prefix):
#                 ret += resultado
#         if self.hijos.items():
#             last_prefix = u''.join([prefix, u'    '])
#             ret += u''.join([prefix, LAST, HORIZONTAL, HORIZONTAL, u' ', self.hijos.items()[-1][0] ])
#             for resultado in self.hijos.items()[-1][1].__str__(prof+1,next_prefix):
#                 ret += resultado
#         return ret
        ret = "[%s]\n" % (self.dato)
        for etiqueta,subarbol in self.hijos.items():
            ret += "%s---(%s)--- %s\n" % ('  '*prof,etiqueta,subarbol.__str__(prof+1))
        return ret
    
# Test
h11 = Nodo(u"h11")
h12 = Nodo(u"h12")
h21 = Nodo(u"h21")
h1 = Nodo(u"h1")
h1.add_hijo(h11,u"soy 11")
h1.add_hijo(h12,u"soy 12")
h2 = Nodo(u"h2")
h2.add_hijo(h21,u"soy 21")
root = Nodo(u"raiz")
root.add_hijo(h1,u"soy 1")
root.add_hijo(h2,u"soy 2")
 
# root.myprint(0)  
print root
