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
    def __init__(self, dato, hijos=[]):
        self.etiqueta = dato
        self.hijos    = hijos
    
    def add_hijo(self, subarbol):
        self.hijos.append(subarbol)

    def print_arbol(self, prof):
        print '  '*prof,self.etiqueta
        for hijo in self.hijos:
            hijo.print_arbol(prof+1)

# Test
# h11 = Nodo("h11")
# h12 = Nodo("h12")
# h21 = Nodo("h21")
# h1 = Nodo("h1",[h11,h12])
# h2 = Nodo("h2",[h21])
# root = Nodo("raiz",[h1,h2])
# 
# root.print_arbol(0)
