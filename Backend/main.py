from flask import Flask, jsonify, request
from flask_cors import CORS
from funtions import *

app = Flask(__name__)
CORS(app)
#load data
@app.route("/load", methods=['POST'])
def loadData():
    #nombre = request.json['nombre']
    #OBTENEMOS LOS DATOS DEL REQUEST
    content = (request.get_data())
    extractData(content)
    xml = analizar_datos()
    # object = {"Mensaje":"Se hizo el POST correctamente"}
    return xml

@app.route("/message", methods=['POST'])
def messageAnalize():
    #OBTENEMOS LOS DATOS DEL REQUEST
    content = (request.get_data())
    xml = analizarMensaje(content)
    return xml

@app.route("/reset", methods=['GET'])
def resetData():
    resultado = reset()
    if resultado:
        mensaje = {"Mensaje":True}
    else:
        mensaje = {"Mensaje":False}
        
    return jsonify(mensaje)

#INICIAR LA APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)