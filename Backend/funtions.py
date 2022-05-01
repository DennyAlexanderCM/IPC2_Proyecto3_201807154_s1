from email.message import Message
from xml.dom.minidom import *

from LinkedList import LinkedList
from message import Message
import re

searchDate = re.compile(r'(\d{2})/(\d{2})/(\d{4})')

txt = """<?xml version="1.0" ?>
<base_de_datos>
	<palabras_positivas>
	</palabras_positivas>
	<palabras_negativas>
	</palabras_negativas>
	<empresas>
	</empresas>
	<lista_mensajes>
	</lista_mensajes>
</base_de_datos>"""

#extraemos los datos y las almacenamos en 
def extractData(xml):
    #CONVERTIMOS EL ARCHIVO DE TEXTO EA UN ARCHIVO XML
    doc = parseString(xml)
    #ELEMENTO RAIZ DEL ARCHIVO
    rootNode = doc.documentElement
    pFeelings = rootNode.getElementsByTagName('sentimientos_positivos')[0].getElementsByTagName('palabra')
    nFeelings = rootNode.getElementsByTagName('sentimientos_negativos')[0].getElementsByTagName('palabra')
    companies = rootNode.getElementsByTagName('empresa')
    message = rootNode.getElementsByTagName('mensaje')
    
    #------------ESCRITURA EN LA BASE DE DATOS
    bd = parse('bd.xml')
    rootNodeBd = bd.documentElement
    pos = rootNodeBd.getElementsByTagName('palabras_positivas')[0]
    negative = rootNodeBd.getElementsByTagName('palabras_negativas')[0]
    messageBd = rootNodeBd.getElementsByTagName('lista_mensajes')[0]
    comp = rootNodeBd.getElementsByTagName('empresas')[0]
    
    for data in pFeelings:
        element = bd.createElement("palabra")
        element.appendChild(doc.createTextNode(data.firstChild.data))
        pos.appendChild(element)
    
    for data in nFeelings:
        element = bd.createElement("palabra")
        element.appendChild(doc.createTextNode(data.firstChild.data))
        negative.appendChild(element)

    for data in message:
        msg = data.firstChild.data
        msg = cleanMessage(msg)
        value = searchDate.search(msg)
        element = bd.createElement("mensaje")
        element.setAttribute("fecha",value[0] )
        element.appendChild(doc.createTextNode(msg))
        messageBd.appendChild(element)
    
    
    for data in companies:
        name = data.getElementsByTagName('nombre')[0].firstChild.data
        element = bd.createElement("empresa")
        element.setAttribute("nombre"  , name)
        service = data.getElementsByTagName('servicio')
        for aux_1 in service:
            aux_2 = aux_1.getElementsByTagName('alias')
            sub_element = bd.createElement("servicio")
            sub_element.setAttribute("nombre"  , aux_1.getAttribute("nombre"))
            for j in aux_2:
                sub_sub_element = bd.createElement("alias")
                sub_sub_element.appendChild(doc.createTextNode(j.firstChild.data))
                sub_element.appendChild(sub_sub_element)
            element.appendChild(sub_element)
        comp.appendChild(element)
    
    bd = cleanDate(bd)
    xml = Node.toprettyxml(bd)
    f =  open("bd.xml", "w", encoding='utf-8')    
    f.write(xml)
    f.close()

    return xml

def cleanDate(xml):
    txt = Node.toxml(xml)
    txt = txt.replace("\t", "")
    txt = txt.replace("  ", "")
    txt = txt.replace("   ", "")
    txt = txt.replace("    ", "")
    txt = txt.replace("     ", "")
    txt = txt.replace("\n", "")
    txt = txt.replace("\r", "")
    xml_2 = parseString(txt)
    return xml_2

def cleanMessage(msg):
    txt = msg
    txt = txt.replace("\t", " ")
    txt = txt.replace("  ", " ")
    txt = txt.replace("   ", " ")
    txt = txt.replace("    ", " ")
    txt = txt.replace("     ", " ")
    txt = txt.replace("\n", " ")
    txt = txt.replace("\r", " ")
    return txt

def clasificarMensajes():
    bd = parse('bd.xml')
    rootNodeBd = bd.documentElement
    messages = rootNodeBd.getElementsByTagName('lista_mensajes')[0].getElementsByTagName('mensaje')


def analizar_datos():
    #EXPRECIÓN REGULAR PARA BUSCAR FECHAS
    
    message_list = LinkedList()
    bd = parse('bd.xml')
    rootNodeBd = bd.documentElement
    pos = rootNodeBd.getElementsByTagName('palabras_positivas')[0].getElementsByTagName('palabra')
    negative = rootNodeBd.getElementsByTagName('palabras_negativas')[0].getElementsByTagName('palabra')
    messages = rootNodeBd.getElementsByTagName('lista_mensajes')[0].getElementsByTagName('mensaje')
    comp = rootNodeBd.getElementsByTagName('empresa')

    #RECORREMOS LA LISTA DE EMPRESAS
    for empresa in comp:
            #OBTENEMOS EL NONMBRE DE LA EMPRESA
            nombreEmpresa = empresa.getAttribute("nombre")

            #LISTAMOS LOS SERVICIOS
            serviciosEmpresa = empresa.getElementsByTagName('servicio')
            tot = 0

            for message in messages:
                #CAMBIAMOS EL FORMATO REEMPLZANDO CARACTERES CON TILDES
                mensaje_leido = normalize((message.firstChild.data).lower())
                #BUSCAMOS SI SE MENCIONA LA EMPRESA EN EL MENSAJE
                nombre_empresa = normalize(nombreEmpresa.lower())
                busqueda = re.search(nombre_empresa.strip(), mensaje_leido)

                if busqueda != None:
                    tot += 1
                    positive_n = 0
                    negative_n = 0
                    #CONTAMOS LAS PALABRAS POSITIVAS
                    for positive in pos:
                        buscar = (positive.firstChild.data).lower()
                        buscar = normalize(buscar.strip())
                        x = re.search(buscar, mensaje_leido)
                        if x:
                            positive_n += 1
        
                    #CONTAMOS LAS PALABRAS NEGATIVAS
                    for negt in negative:
                        buscar = (negt.firstChild.data).lower()
                        buscar = normalize(buscar.strip())
                        x = re.search(buscar, mensaje_leido)
                        if x:
                            negative_n += 1
                    
                    #RECORREMOS LA LISTA DE SERVICIOS DE LA EMPRESA
                    for servicioEmpresa in serviciosEmpresa:
                        #OBTENEMOS EL NOMBRE DEL SERVICIO
                        nombreServicio = servicioEmpresa.getAttribute("nombre")
                        #LISTAMOS LOS ALIAS DISPONIBLES
                        alias = servicioEmpresa.getElementsByTagName('alias')
                        #CAMBIAMOS EL FORMATO
                        buscar = normalize(nombreServicio.strip())
                        search = re.search(buscar, mensaje_leido)
                        if search is None:
                            total_Service = 1
                            for palabra in alias:
                                buscar_palabra = normalize((palabra.firstChild.data).strip())
                                busqueda_palabra = re.search(buscar_palabra, mensaje_leido)
                                if busqueda_palabra != None:
                                    print(nombreServicio)
                                    break

                        else:
                            print(nombreServicio)
                        
            
            
            
            
            """
            
            
3

    for message in messages:
        
        
        #BUSCAMOS LA FECHA
        fecha = date.search(mensaje_leido)"""

        

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.lower(), b.lower())
    return s



def returnData():
    xml = '<?xml version="1.0" ?><lista_respuestas></lista_respuestas>'
    doc = parse(xml)
    rootNode = doc.documentElement
    lista_respuestas = rootNode.getElementsByTagName('lista_respuestas')[0]



fecha = """Lugar y fecha: Guatemala, 31/12/2022 15:01 Usuario: 
	  map0001@usac.edu   Red social: Twitter
	  El servicio en la USAC para inscripción fue muy bueno y me siento muy satisfecho."""

fdate = re.compile(r'([0][1-9]|[12][0-9]|3[01])(\/|-)([0][1-9]|[1][0-2])\2(\d{4})(\s)([0-1][1-9]|[2][0-3])(:)([0-5][0-9])')


result =fdate.search(fecha)