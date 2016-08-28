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

class Nodo:

    def __init__(self, dato):
        self.etiqueta = dato
        self.hijos = []

    def add_hijo(self, valor, subarbol):
        self.hijos.append(subarbol)

    def __str__(self,prof=0):
        ret = "%s %s\n" % ('  '*prof,self.etiqueta)
        for hijo in self.hijos:
            ret += hijo.__str__(prof+1)
        return ret

# Test
# h11 = Nodo("h11")
# h12 = Nodo("h12")
# h21 = Nodo("h21")
# h1 = Nodo("h1")
# h1.add_hijo(h11)
# h1.add_hijo(h12)
# h2 = Nodo("h2")
# h2.add_hijo(h21)
# root = Nodo("raiz")
# root.add_hijo(h1)
# root.add_hijo(h2)
#
# # root.myprint(0)
# print root
