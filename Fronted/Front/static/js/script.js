var xmlFile = " "
var mensaje = ""
/*FUNCIÓN PARA MOSTRAR EL MENÚ DE SUBIR ARCHIVO*/
function showDiv2() {
    var div2 = document.getElementById("div_2");
    document.getElementById("div_1").style.display = "none";
    document.getElementById("div_3").style.display = "none";
    document.getElementById("div_4").style.display = "none";
    document.getElementById("div_5").style.display = "none";
    document.getElementById("div_6").style.display = "none";
    if (div2.style.display === "none") {
        div2.style.display = "flex";
    }
}
function showDiv3() {
    var div3 = document.getElementById("div_3");
    document.getElementById("div_1").style.display = "none";
    document.getElementById("div_2").style.display = "none";
    document.getElementById("div_4").style.display = "none";
    document.getElementById("div_5").style.display = "none";
    document.getElementById("div_6").style.display = "none";
    if (div3.style.display === "none") {
        div3.style.display = "flex";
    }
}
function showDiv4() {
    var div4 = document.getElementById("div_4");
    document.getElementById("div_1").style.display = "none";
    document.getElementById("div_2").style.display = "none";
    document.getElementById("div_3").style.display = "none";
    document.getElementById("div_5").style.display = "none";
    document.getElementById("div_6").style.display = "none";
    if (div4.style.display === "none") {
        div4.style.display = "flex";
    }
}
function showDiv5() {
    var div5 = document.getElementById("div_5");
    document.getElementById("div_1").style.display = "none";
    document.getElementById("div_2").style.display = "none";
    document.getElementById("div_3").style.display = "none";
    document.getElementById("div_4").style.display = "none";
    document.getElementById("div_6").style.display = "none";
    if (div5.style.display === "none") {
        div5.style.display = "flex";
    }
}
function showDiv6() {
    var div6 = document.getElementById("div_4");
    document.getElementById("div_1").style.display = "none";
    document.getElementById("div_2").style.display = "none";
    document.getElementById("div_3").style.display = "none";
    document.getElementById("div_4").style.display = "none";
    document.getElementById("div_5").style.display = "none";
    if (div6.style.display === "none") {
        div6.style.display = "flex";
    }
}
/*Función para leer archivos xml*/
function readXML() {
    //VARIABLES PARA LA LECTURA DEL ARCHIVO
    var text, parser, xmlDoc, pFeelings, pos, negativos;

    parser = new DOMParser();
    xmlDoc = parser.parseFromString(xml, "text/xml");
    negativos = (xmlDoc.getElementsByTagName("sentimientos_negativos")[0].getElementsByTagName("palabra"))
    pos = (xmlDoc.getElementsByTagName("sentimientos_positivos")[0].getElementsByTagName("palabra"))
    console.log(pos.length)


    for (i = 0; i < pos.length; i++) {
        console.log(pos[i].childNodes[0].nodeValue)
    }
    for (i = 0; i < negativos.length; i++) {
        console.log(negativos[i].childNodes[0].nodeValue)
    }
    document.getElementById("demo").innerHTML =
        xmlDoc.getElementsByTagName("palabra")[0].childNodes[0].nodeValue;
}

function readFile(evt) {
    let fileField1 = evt.target.files[0];
    let reader = new FileReader();
    reader.onload = (e) => {
        //Alerta con sweet alert 
        alerta("¡Archivo cargado!", 'success')
        texto('textarea', e.target.result)
        xmlFile = e.target.result
    };
    // Leemos el contenido del archivo seleccionado
    reader.readAsText(fileField1, "utf-8");
}
document.getElementById('inputfile').addEventListener('change', readFile, false);

function alerta(mensaje, tipo) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: tipo,
        title: mensaje
    })
}


function enviar() {
    var objeto = xmlFile

    if (objeto != " ") {
        fetch(' http://192.168.0.105:3000/load', {
            method: 'POST',
            body: objeto,
            headers: {
                'Content-Type': 'application/xml',
                'Access-Control-Allow-Origin': '*',
            }
        })

            .then(res => res.text())
            .catch(err => {
                console.error('Error:', err)
                alert("Ocurrio un error, ver la consola")
            })
            /* ULTIMA TRANSFORMACION
                Si el metodo funciono correctamente y se logro transformar la respuesta en un JSON, hara lo que este dentro de las llaves.
            */
            .then(response => {
                // En este apargado, se haran las acciones si la respuesta fue correcta basicamente.
                alerta('Archivo Cargado', 'success')
                texto('resultados', response)
                // Usamos un alert, para desplegar un mensaje en pantalla de parte del navegador
                // Esto se puede reemplazar con mas librerias.
            })
    }
    else {
        alerta('Sin archivo seleccionado', 'error')
    }

}

function texto(id, value) {
    document.getElementById(id).value = value;
}

// --------------INGRESO DEL MENSAJE
function readFile_2(evt) {
    let fileField2 = evt.target.files[0];
    let reader = new FileReader();
    reader.onload = (e) => {
        //Alerta con sweet alert 
        alerta("¡Archivo cargado!", 'success')
        mensaje = e.target.result
    };
    // Leemos el contenido del archivo seleccionado
    reader.readAsText(fileField2, "utf-8");
}
document.getElementById('inputfileMessage').addEventListener('change', readFile_2, false);

function enviarMensaje() {
    var objeto = mensaje

    if (objeto != "") {
        fetch('http://192.168.0.105:3000/message', {
            method: 'POST',
            body: objeto,
            headers: {
                'Content-Type': 'application/xml',
                'Access-Control-Allow-Origin': '*',
            }
        })

            .then(res => res.text())
            .catch(err => {
                console.error('Error:', err)
                alert("Ocurrio un error, ver la consola")
            })
            /* ULTIMA TRANSFORMACION
                Si el metodo funciono correctamente y se logro transformar la respuesta en un JSON, hara lo que este dentro de las llaves.
            */
            .then(response => {
                // En este apargado, se haran las acciones si la respuesta fue correcta basicamente.
                alerta('Archivo Cargado', 'success')
                texto('resultadosMensaje', response)
                // Usamos un alert, para desplegar un mensaje en pantalla de parte del navegador
                // Esto se puede reemplazar con mas librerias.
            })
    }
    else {
        alerta('Sin archivo seleccionado', 'error')
    }

}

//-----------------------RESEt
function reset() {
    fetch('http://192.168.0.105:3000/reset', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        }
    })
        .then(res => res.json())
        .catch(err => {
            console.error('Error:', err)
            alert("Ocurrio un error, ver la consola")
        })
        .then(response => {
            console.log(response);
            valor = response.Mensaje
            if (valor == true){
                alerta('Completado, datos reiniciados', 'success')
            } else{
                alerta('Error, a ocurrido un error', 'error')
            }
        })
}
