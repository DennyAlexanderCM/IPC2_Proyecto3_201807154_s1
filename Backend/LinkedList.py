from message import Message
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
    
class LinkedListDates:
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
            if self.verificar(data):
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
    
    def sortList(self):
        end = None
        while end != self.head:
            aux = self.head
            while aux .next != end:
                q = aux .next
                if aux.data > q.data:
                    aux.data, q.data = q.data, aux.data
                aux = aux.next
            end = aux
    
    def verificar(self, date):
        repetido = True
        aux = self.head
        while aux:
            if date == aux.data:
                repetido = False
            aux = aux.next
        return repetido
    
    def print(self):
        aux = self.head
        while aux:
            print(aux.data)
            aux = aux.next