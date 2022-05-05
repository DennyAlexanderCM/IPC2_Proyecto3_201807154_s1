from xml.dom.minidom import *
from LinkedList import LinkedList, LinkedListDates
from message import Message
import xmltodict
import re
import json

#EXPRESIONES REGUALRES
buscarRed = re.compile(r'(([Ss][Oo][Cc][Ii][Aa][lL]:))\s?[a-zA-Z0-9]+')
buscarUsuario = re.compile(r'(([Uu][Ss][Uu][Aa][Rr][Ii][Oo]:))\s*?[^\s]+')
#EXPRESIÓN REGULAR PARA BUSCAR FECHAS EN UN STRING
searchDate = re.compile(r'(\d{2})/(\d{2})/(\d{4})')

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
        element.appendChild(bd.createTextNode(data.firstChild.data))
        pos.appendChild(element)
    
    for data in nFeelings:
        element = bd.createElement("palabra")
        element.appendChild(bd.createTextNode(data.firstChild.data))
        negative.appendChild(element)
    
    for data in message:
        msg = data.firstChild.data
        msg = cleanMessage(msg)
        element = bd.createElement("mensaje")
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
                sub_sub_element.appendChild(bd.createTextNode(j.firstChild.data))
                sub_element.appendChild(sub_sub_element)
            element.appendChild(sub_element)
        comp.appendChild(element)
    
    #GUARDAMOS LOS DATOS EN LA BD
    bd = cleanDate(bd)
    xml = Node.toprettyxml(bd)
    f =  open("bd.xml", "w", encoding='utf-8')    
    f.write(xml)
    f.close()

def cleanDate(xml):
    txt = Node.toxml(xml)
    txt = txt.replace("\t", "")
    txt = txt.replace("\n", "")
    txt = txt.replace("\r", "")
    txt = txt.replace("   ", "")
    txt = txt.replace("    ", "")
    txt = txt.replace("     ", "")
    xml_2 = parseString(txt)
    return xml_2

def cleanMessage(msg):
    txt = msg
    txt = txt.replace("\t", " ")
    txt = txt.replace("\n", " ")
    txt = txt.replace("\r", " ")
    return txt

def estadoMensajes(mensaje):
    estado = "neutro"
    #CAMBIAMOS EL FORMATO DEL MENSAJE PARA SU MEJOR LECTURA
    mensaje_leido = normalize(mensaje.lower())
    #ABRIMOS LA BASE DE DATOS
    bd = parse('bd.xml')
    rootNode = bd.documentElement
    pos = rootNode.getElementsByTagName('palabras_positivas')[0].getElementsByTagName('palabra')
    negative = rootNode.getElementsByTagName('palabras_negativas')[0].getElementsByTagName('palabra')
    
    positive_n = 0
    negative_n = 0
    
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

    if positive_n > negative_n:
        estado = "positivo"
    elif positive_n < negative_n:
        estado = "negativo"
    return estado

def analizar_datos():
    #LISTA DE MENSAJES
    messageList = LinkedList()
    datesList = LinkedListDates()

    response = parseString('<?xml version="1.0"?><lista_respuestas></lista_respuestas>')
    #ACCEDEMOS A LA BASE DE DATOS
    bd = parse('bd.xml')
    rootNode = bd.documentElement
    respuestas = response.getElementsByTagName('lista_respuestas')[0]
    comp = rootNode.getElementsByTagName('empresa')
    mensajeBd = rootNode.getElementsByTagName('mensaje')
    
    for data in mensajeBd:
        objectMensaje = Message()
        msg = data.firstChild.data
        msg = cleanMessage(msg)
        estado = estadoMensajes(msg)
        value = searchDate.search(msg)
        objectMensaje.setFecha(value[0])
        objectMensaje.setMessage(msg)
        objectMensaje.setEstado(estado)
        messageList.append(objectMensaje)
        datesList.append(value[0])

    #RECORREMOS POR FECHAS
    aux = datesList.head
    while aux:
        sum_total = 0
        sum_pos = 0
        sum_neg = 0
        sum_neutro = 0
        mensaje = response.createElement("mensajes")
        respuesta = response.createElement("respuesta")
        fecha = response.createElement("fecha")
        fecha.appendChild(response.createTextNode(aux.data))
        respuesta.appendChild(fecha)
        print("Para la fecha: "+aux.data)
        
        for empresa in comp:
            analisis = response.createElement("analisis")
            #OBTENEMOS EL NONMBRE DE LA EMPRESA
            nombreEmpresa = empresa.getAttribute("nombre")
            #LISTAMOS LOS SERVICIOS
            serviciosEmpresa = empresa.getElementsByTagName('servicio')
            tot = 0
            neutro = 0
            positive_n = 0
            negative_n = 0

            company = response.createElement("empresa")
            company.setAttribute("nombre"  , nombreEmpresa)
            sub_mensaje = response.createElement("mensaje")
            servicios = response.createElement("servicios")
            
            #RECORREMOS LA LISTA DE SERVICIOS DE LA EMPRESA
            for servicioEmpresa in serviciosEmpresa:
                
                ntot = 0
                serviceNegative = 0
                servicePositive = 0
                serviceNeutral = 0
                #OBTENEMOS EL NOMBRE DEL SERVICIO
                nombreServicio = servicioEmpresa.getAttribute("nombre")

                servicio = response.createElement("servicio")
                sub_sub_mensaje = response.createElement("mensajes")
                servicio.setAttribute("nombre", nombreServicio)
                #LISTAMOS LOS ALIAS DISPONIBLES
                alias = servicioEmpresa.getElementsByTagName('alias')
                #CAMBIAMOS EL FORMATO
                buscar = normalize(nombreServicio.strip())
                #RECORREMOS LA LISTA DE MENSAJES
                aux_mensajes = messageList.head
                while aux_mensajes:
                    mensaje_leido:Message = aux_mensajes.data
                    #COMPROBAMOS LAS FECHAS
                    if mensaje_leido.fecha == aux.data:
                        #OBTENEMOS EL MENSAJE CON EL FORMATO CORREGIDO
                        mensaje_str = normalize(mensaje_leido.message.lower())
                        #CAMBIAMOS EL FORMATO
                        nombre_empresa = normalize(nombreEmpresa.lower())
                        busqueda = re.search(nombre_empresa.strip(), mensaje_str)
                        #VERIFICAMOS SI SE MENCIONA LA EMPRESA EN EL MENSAJE
                        if busqueda != None:
                            search = re.search(buscar, mensaje_str)
                            if search is None:
                                for palabra in alias:
                                    buscar_palabra = normalize((palabra.firstChild.data).strip())
                                    busqueda_palabra = re.search(buscar_palabra, mensaje_str)
                                    if busqueda_palabra != None:
                                        ntot +=1
                                        tot += 1
                                        sum_total += 1
                                        if mensaje_leido.estado == "positivo":
                                            servicePositive +=1
                                            positive_n += 1
                                            sum_pos += 1
                                        elif mensaje_leido.estado == "negativo":
                                            serviceNegative +=1
                                            negative_n += 1
                                            sum_neg += 1
                                        else:
                                            serviceNeutral+=1
                                            neutro += 1
                                            sum_neutro += 1
                                        break
                            else:
                                ntot +=1
                                tot += 1
                                sum_total += 1
                                if mensaje_leido.estado == "positivo":
                                    servicePositive +=1
                                    positive_n += 1
                                    sum_pos += 1
                                elif mensaje_leido.estado == "negativo":
                                    serviceNegative +=1
                                    negative_n += 1
                                    sum_neg += 1
                                else:
                                    serviceNeutral+=1
                                    neutro += 1
                                    sum_neutro += 1
                    aux_mensajes = aux_mensajes.next
                
                total = response.createElement("total")
                total.appendChild(response.createTextNode(str(ntot)))
                sub_sub_mensaje.appendChild(total)
                positivos = response.createElement("positivos")
                positivos.appendChild(response.createTextNode(str(servicePositive)))
                sub_sub_mensaje.appendChild(positivos)
                negativos = response.createElement("negativos")
                negativos.appendChild(response.createTextNode(str(serviceNegative)))
                sub_sub_mensaje.appendChild(negativos)
                res_neutros = response.createElement("neutros")
                res_neutros.appendChild(response.createTextNode(str(serviceNeutral)))
                sub_sub_mensaje.appendChild(res_neutros)

                servicio.appendChild(sub_sub_mensaje)
                servicios.appendChild(servicio)
                print(ntot, servicePositive, serviceNegative, serviceNeutral)
            
            total = response.createElement("total")
            total.appendChild(response.createTextNode(str(tot)))
            sub_mensaje.appendChild(total)
            positivos = response.createElement("positivos")
            positivos.appendChild(response.createTextNode(str(positive_n)))
            sub_mensaje.appendChild(positivos)
            negativos = response.createElement("negativos")
            negativos.appendChild(response.createTextNode(str(negative_n)))
            sub_mensaje.appendChild(negativos)
            res_neutros = response.createElement("neutros")
            res_neutros.appendChild(response.createTextNode(str(neutro)))
            sub_mensaje.appendChild(res_neutros)
            company.appendChild(sub_mensaje)
            company.appendChild(servicios)
            analisis.appendChild(company)           
            print(tot, positive_n,negative_n, neutro)

        total = response.createElement("total")
        total.appendChild(response.createTextNode(str(tot)))
        mensaje.appendChild(total)
        positivos = response.createElement("positivos")
        positivos.appendChild(response.createTextNode(str(positive_n)))
        mensaje.appendChild(positivos)
        negativos = response.createElement("negativos")
        negativos.appendChild(response.createTextNode(str(negative_n)))
        mensaje.appendChild(negativos)
        res_neutros = response.createElement("neutros")
        res_neutros.appendChild(response.createTextNode(str(neutro)))
        mensaje.appendChild(res_neutros)
        respuesta.appendChild(mensaje)
        respuesta.appendChild(analisis)
        respuestas.appendChild(respuesta)
        aux = aux.next

    response = cleanDate(response)
    xml = Node.toprettyxml(response)
    
    f =  open("dates.xml", "w", encoding='utf-8')    
    f.write(xml)
    f.close()
    return xml

def analizarMensaje(mensaje):
    #RAIZ DEL RESULTADO
    respuestaXml = parseString('<?xml version="1.0"?><respuesta></respuesta>')
    respuesta = respuestaXml.getElementsByTagName('respuesta')[0]
    #CONVERTIMOS EL ARCHIVO DE TEXTO EN UN ARCHIVO XML
    doc = parseString(mensaje)
    #ELEMENTO RAIZ DEL ARCHIVO
    message = doc.getElementsByTagName('mensaje')[0]
    #OBTENMOS EL MENSAJE
    msg = message.firstChild.data
    msg = cleanMessage(msg)

    #------------ABRIMOS LA BASE DE DATOS
    bd = parse('bd.xml')
    rootNode = bd.documentElement
    pos = rootNode.getElementsByTagName('palabras_positivas')[0]
    negative = rootNode.getElementsByTagName('palabras_negativas')[0]
    empresas = rootNode.getElementsByTagName('empresa')

    #OBTENEMOS LOS DATOS DEL MENSAJE
    fecha = searchDate.search(msg)[0]
    fechaXml = respuestaXml.createElement("fecha")
    fechaXml.appendChild(respuestaXml.createTextNode(fecha))
    respuesta.appendChild(fechaXml)
    usuario= buscarUsuario.search(msg)[0].split(':')
    usuarioXml = respuestaXml.createElement("usuario")
    usuarioXml.appendChild(respuestaXml.createTextNode(usuario[1]))
    respuesta.appendChild(usuarioXml)
    red = buscarRed.search(msg)[0].split(':')
    redXml = respuestaXml.createElement("red_social")
    redXml.appendChild(respuestaXml.createTextNode(red[1]))
    respuesta.appendChild(redXml)
    empresasXml = respuestaXml.createElement("empresas")

    #RECORREMOS LA LISTA DE EMPRESAS
    for empresa in empresas:
        #OBTENEMOS EL NONMBRE DE LA EMPRESA
        nombreEmpresa = empresa.getAttribute("nombre")
        #LISTAMOS LOS SERVICIOS
        serviciosEmpresa = empresa.getElementsByTagName('servicio')
        #OBTENEMOS EL MENSAJE CON EL FORMATO CORREGIDO
        mensaje_str = normalize(msg.lower())
        #CAMBIAMOS EL FORMATO
        nombre_empresa = normalize(nombreEmpresa.lower())
        busqueda = re.search(nombre_empresa.strip(), mensaje_str)
        #VERIFICAMOS SI SE MENCIONA LA EMPRESA EN EL MENSAJE
        if busqueda:
            company = respuestaXml.createElement("empresa")
            company.setAttribute("nombre"  , nombreEmpresa)
            #RECORREMOS LA LISTA DE SERVICIOS DE LA EMPRESA
            for servicioEmpresa in serviciosEmpresa:
                #OBTENEMOS EL NOMBRE DEL SERVICIO
                nombreServicio = servicioEmpresa.getAttribute("nombre")
                #LISTAMOS LOS ALIAS DISPONIBLES
                alias = servicioEmpresa.getElementsByTagName('alias')
                #CAMBIAMOS EL FORMATO
                nombre_servicio = normalize(nombreServicio.lower())
                busqueda_2 = re.search(nombre_servicio.strip(), mensaje_str)
                if busqueda_2 is None:
                    for palabra in alias:
                        buscar_palabra = normalize((palabra.firstChild.data).lower())
                        busqueda_3 = re.search(buscar_palabra.strip(), mensaje_str)
                        if busqueda_3:
                            servicio = respuestaXml.createElement("servicio")
                            servicio.appendChild(respuestaXml.createTextNode(nombreServicio))
                            company.appendChild(servicio)
                            break
                else:
                    servicio = respuestaXml.createElement("servicio")
                    servicio.appendChild(respuestaXml.createTextNode(nombreServicio))
                    company.appendChild(servicio)
            empresasXml.appendChild(company)
            respuesta.appendChild(empresasXml)
    
    positive_n = positivos(msg)
    negative_n = negativos(msg)

    tot = float(positive_n + negative_n)

    posXml = respuestaXml.createElement("palabras_positivas")
    posXml.appendChild(respuestaXml.createTextNode(str(positive_n)))
    respuesta.appendChild(posXml)
    negXml = respuestaXml.createElement("palabras_negativas")
    negXml.appendChild(respuestaXml.createTextNode(str(negative_n)))
    respuesta.appendChild(negXml)
    
    porcentajeP = 100*(positive_n/tot)
    porcentajeN = 100*(negative_n/tot)

    porcentajeXml = respuestaXml.createElement("sentimiento_positivo")
    porcentajeXml.appendChild(respuestaXml.createTextNode(str(porcentajeP)+" %"))
    respuesta.appendChild(porcentajeXml)
    porcentajeNegXml = respuestaXml.createElement("sentimiento_negativo")
    porcentajeNegXml.appendChild(respuestaXml.createTextNode(str(porcentajeN)+" %"))
    respuesta.appendChild(porcentajeNegXml)

    estado = estadoMensajes(msg)
    analizado = respuestaXml.createElement("sentimiento_analizado")
    analizado.appendChild(respuestaXml.createTextNode(estado))
    respuesta.appendChild(analizado)

    xml = Node.toprettyxml(respuestaXml)
    return xml

def positivos(mensaje):
    #CAMBIAMOS EL FORMATO DEL MENSAJE PARA SU MEJOR LECTURA
    mensaje_leido = normalize(mensaje.lower())
    #ABRIMOS LA BASE DE DATOS
    bd = parse('bd.xml')
    rootNode = bd.documentElement
    pos = rootNode.getElementsByTagName('palabras_positivas')[0].getElementsByTagName('palabra')
    
    positive_n = 0
    
    for positive in pos:
        buscar = (positive.firstChild.data).lower()
        buscar = normalize(buscar.strip())
        x = re.search(buscar, mensaje_leido)
        if x:
            positive_n += 1
    
    return positive_n

def negativos(mensaje):
    #CAMBIAMOS EL FORMATO DEL MENSAJE PARA SU MEJOR LECTURA
    mensaje_leido = normalize(mensaje.lower())
    #ABRIMOS LA BASE DE DATOS
    bd = parse('bd.xml')
    rootNode = bd.documentElement
    pos = rootNode.getElementsByTagName('palabras_negativas')[0].getElementsByTagName('palabra')
    
    negative_n = 0
    
    for positive in pos:
        buscar = (positive.firstChild.data).lower()
        buscar = normalize(buscar.strip())
        x = re.search(buscar, mensaje_leido)
        if x:
            negative_n += 1
    
    return negative_n

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


def reset():
    txt = """<?xml version="1.0" ?><base_de_datos>
	<palabras_positivas>
	</palabras_positivas>
	<palabras_negativas>
	</palabras_negativas>
	<empresas>
	</empresas>
    <lista_mensajes>
	</lista_mensajes>
</base_de_datos>"""
    #GUARDAMOS LOS DATOS EN LA BD
    f =  open("bd.xml", "w", encoding='utf-8')    
    f.write(txt)
    f.close()

    f =  open("dates.xml", "w", encoding='utf-8')    
    f.write('')
    f.close()

    return True