//https://geekflare.com/es/handling-files-in-javascript/

import express from 'express';
import fs from 'fs';
import { spawn } from 'child_process';

const app = express();
app.use(express.json());

// Configura CORS para permitir solicitudes desde tu Live Server
app.use((req, res, next) => {
	res.header('Access-Control-Allow-Origin', 'http://127.0.0.1:5500'); // <--- Es vital que esta URL sea la de tu Live Server
	res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
	res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
	next();
  });

  let txtEnvio = ""
  let iAnswer = {
    pedido: "",
    nombreArchivos: [],
    tipoArchivos: "",
    ubicacion: "",
    txtAIngrsr: "",
  }
  let ubint = ""
  let respuesta = ""
  let funcionAplicar
  app.post('/echo', (req, res) => {
    // spawn recibe el comando a ejecutar y los argumentos, es similar a utilizar desde línea de comandos "python script_python.py"
	const pythonProcess = spawn('python', ['python.py'])
	let pythonResponse = ""


    // stdout: Se encarga de la salida de datos del stdout del subproceso. En este caso, recibe datos del subproceso de Python.
	// .stdout.on('data',…): Ejecuta una función especificada cuando se reciben los datos que envía el subproceso.
	pythonProcess.stdout.on('data', function(data) {
		pythonResponse += data.toString()
	})
	// .stdout.on('end',…): Ejecuta una función especificada cuando se terminan de recibir datos desde el subproceso.
	pythonProcess.stdout.on('end', function() {
		 // Ahora parseamos el JSON completo
		 const parsed = JSON.parse(pythonResponse);

		 // Ejemplo: supongamos que el Python envía un objeto
		iAnswer = parsed


    //aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; 
    if(iAnswer.nombreArchivos[0] != null){
      for(let i = 0; i < nombreArchivos.lenght; i++){
        funcionAplicar(iAnswer.ubicacion, iAnswer.nombreArchivos[i])
      }
    }

  })

    	// stdin: Se encarga del ingreso de datos al stdin del subproceso. En este caso, envía datos del subproceso de Python.
	// .stdin.write(datos): Envía datos al subproceso
	pythonProcess.stdin.write(req.body.prompt)
	// .stdin.end(): Indica al subproceso que el envío de datos finalizó para que pueda ejecutar sus acciones
	pythonProcess.stdin.end()

  
  });















  function cambia (carpeta, archivoAC){
      fs.readFile(carpeta + archivoAC, (err, contenido) =>{
        if(err){
          respuesta =  `Lo lamento, no encuento un archivo llamado ${archivoAC} en ${carpeta}. ¿Tal vez esta en otro lado? ¿Tal vez tiene un nombre similar? `
          return;
        }

        let coso = contenido.toString()
        const pythonProcess2 = spawn('python', ['python.py'])
        let pythonResponse2 = ""
        pythonProcess2.stdout.on('data', function(data) {
          pythonResponse2 += data.toString()
        })
        pythonProcess2.stdout.on('end', function(){
          fs.writeFile(carpeta + archivoAC, coso, (err) => {
            if (err) throw err;
            respuesta = "Listo, ya agregamos tu pedido al texto"
          })
        })
      })
  }
function elimina (carpeta, archivoAE){
  fs.unlink(carpeta + archivoAE, (err) =>{
    if(err){
      respuesta = `Lo lamentamos, el archivo que desea eliminar no existe. Intenta ver si esta en otra carpeta o posee un nombre similar`
      return;
    }
    respuesta = `${archivoAE} fue eliminado exitosamente.`
  })
}
function copiar (carpetaVieja, carpetaNueva, archivoACo){
  let coso = ""
  fs.readFile(carpetaVieja + archivoACo, (err, contenido) =>{
    if(err){
      respuesta = `Lo lamentamos, el archivo al que desea aplicarle la operacion no existe, revisa si se encuentra en otra carpeta o si tiene un nombre similar`
      return;
    }
    coso = contenido.toString()
  })
  fs.writeFile(carpetaNueva + archivoACo, coso, (err) =>{
    if (err) throw err;
  console.log("¡Completado!");
  });
}
function mover (carpetadelaquehayquesacar, carpetaenlaquehayqueponer, archivoAM){
  copiar(carpetadelaquehayquesacar, carpetaenlaquehayqueponer, archivoAM, (err) => {
    if (err) {
      console.log("Error en copiar:", err.message);
      return; // 🚨 No seguimos si copiar falla
    }
    elimina(origen, archivo); // solo se llama si copiar tuvo éxito
  });
}