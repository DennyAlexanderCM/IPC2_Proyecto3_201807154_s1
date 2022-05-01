from email import message


class Message:
    def __init__(self):
        self.id = 0
        self.fecha = None
        self.empresa = None
        self.servicios = None
        self.pos = 0
        self.negs = 0
        self.message = None
    
    def setId(self,id):
        self.id = id
    
    def setFecha(self, fecha):
        self.fecha = fecha
    
    def setEmpresa(self, empresa):
        self.empresa = empresa

    def setServicios(self, servicios):
        self.servicios = servicios
    
    def setPos(self, pos):
        self.pos = pos
    
    def setNegs(self, negs):
        self.negs = negs
    
    def setMessage(self, message):
        self.message = message