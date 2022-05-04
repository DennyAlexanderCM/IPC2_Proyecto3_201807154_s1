class Message:
    def __init__(self):
        self.fecha = None
        self.estado = None
        self.message = None
        
    def setFecha(self, fecha):
        self.fecha = fecha
    
    def setEstado(self, estado):
        self.estado = estado
    
    def setMessage(self, message):
        self.message = message