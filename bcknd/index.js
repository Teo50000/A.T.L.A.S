//https://geekflare.com/es/handling-files-in-javascript/

import express from 'express';
import fs from 'fs';
import { spawn } from 'child_process';
import manejoarch from './manejoarchivos';

const app = express();
app.use(express.json());

// Configura CORS para permitir solicitudes desde tu Live Server
app.use((req, res, next) => {
	res.header('Access-Control-Allow-Origin', 'http://127.0.0.1:5500'); // <--- Es vital que esta URL sea la de tu Live Server
	res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
	res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
	next();
  });

  let iAnswer = {
    pedido: "",
    nombreArchivos: [],
    tipoArchivos: "",
    ubicacion_es: [],
    txtAIngrsr: "",
  }
  
  let iAnswerTipo = {
    pedido: "",
    terminacion: [],
    ubicacion_es: [],
    ubicacion_es2: [],
    fecha: "",
    condicion_es: []
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
    if(parsed.nombreodeterminante === "nombre"){
		iAnswer = parsed
      if(iAnswer.pedido === "cambia" || iAnswer.pedido === "elimina"){
          if(iAnswer.pedido === "cambia"){
            funcionAplicar = manejoarch.cambia
          } else{
            funcionAplicar = manejoarch.elimina
          }
        for(let i = 0; i < iAnswer.nombreArchivos.length; i++){
          funcionAplicar(iAnswer.ubicacion_es[i], iAnswer.nombreArchivos[i]);
        }
      } else if(iAnswer.pedido === "copiar" || iAnswer.pedido === "mover"){
        if(iAnswer.pedido = "copiar"){
          funcionAplicar = manejoarch.copiar
        } else{
          funcionAplicar = manejoarch.mover
        }
        for(let i = 0; i < iAnswer.nombreArchivos.length; i++){
          funcionAplicar(iAnswer.ubicacion_es[i], iAnswer.nombreArchivos[i], iAnswer.ubicacion_es2[i]);
        }
      }
    } else if  (nombreodeterminante === "determinante"){
      iAnswerTipo = parsed
    }

    //aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; aca empieza el manejo de archivos; 
    

  })

    	// stdin: Se encarga del ingreso de datos al stdin del subproceso. En este caso, envía datos del subproceso de Python.
	// .stdin.write(datos): Envía datos al subproceso
	pythonProcess.stdin.write(req.body.prompt)
	// .stdin.end(): Indica al subproceso que el envío de datos finalizó para que pueda ejecutar sus acciones
	pythonProcess.stdin.end()
  });