from flask import Flask, jsonify, request
from funtions import *

app = Flask(__name__)

#load data
@app.route("/load", methods=['POST'])
def loadData():
    #nombre = request.json['nombre']
    content = (request.get_data())
    objet = extractData(content)
    object = {"Mensaje":"Se hizo el POST correctamente"}
    return jsonify(objet)

#INICIAR LA APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)