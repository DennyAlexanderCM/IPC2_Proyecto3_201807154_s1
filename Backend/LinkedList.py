#LISTA DOBLEMENTE ENLAZADA
#CLASE NODO
class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        
        self.head = None
        self.last = None

    #VERIFICAMOS SI LA LISTA ESTA VACÍA
    def emply(self):
        return self.head    

    #AGREGAMOS LOS DATOS AL FINAL
    def append(self, data):
        nodo = Node(data)
        if not self.emply():
            self.head = nodo
            self.last = nodo
        else:
            self.last.next = nodo
            self.last = nodo
    
    #RETORNAR EL NÚMERO DE ELEMENTOS
    def length(self):
        n = 0
        i = self.head
        while i:
            i = i.next
            n+=1
        return n
