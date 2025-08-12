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
    nombreArchivo: "",
    ubicacion: "",
    txtAIngrsr: "",
  }

  app.post('/echo', (req, res) => {
    // spawn recibe el comando a ejecutar y los argumentos, es similar a utilizar desde línea de comandos "python script_python.py"
	const pythonProcess = spawn('python', ['python.py'])
	let pythonResponse = ""


    	// stdin: Se encarga del ingreso de datos al stdin del subproceso. En este caso, envía datos del subproceso de Python.
	// .stdin.write(datos): Envía datos al subproceso
	pythonProcess.stdin.write(req.body.nombre)
	// .stdin.end(): Indica al subproceso que el envío de datos finalizó para que pueda ejecutar sus acciones
	pythonProcess.stdin.end()
  });