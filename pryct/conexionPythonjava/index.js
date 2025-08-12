

import express from 'express';

const app = express();
app.use(express.json());
import fs from 'fs';


// Configura CORS para permitir solicitudes desde tu Live Server
app.use((req, res, next) => {
	res.header('Access-Control-Allow-Origin', 'http://127.0.0.1:5500'); // <--- Es vital que esta URL sea la de tu Live Server
	res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
	res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
	next();
  });

  
// child_process: Módulo que nos permite generar subprocesos.
// spawn: Método que genera un subproceso
import { spawn } from 'child_process';

console.log("jauduiudu")
let a  = ""
let b = ""
app.post('/echo', (req, res) => {

	// spawn recibe el comando a ejecutar y los argumentos, es similar a utilizar desde línea de comandos "python script_python.py"
	const pythonProcess = spawn('python', ['python.py'])
	let pythonResponse = ""


	// stdout: Se encarga de la salida de datos del stdout del subproceso. En este caso, recibe datos del subproceso de Python.
	// .stdout.on('data',…): Ejecuta una función especificada cuando se reciben los datos que envía el subproceso.
	pythonProcess.stdout.on('data', function(data) {
		pythonResponse += data.toString()
		let qwert = pythonResponse.trim().split('\n');
		a = qwert[1]
		b = qwert[0]
	})
	// .stdout.on('end',…): Ejecuta una función especificada cuando se terminan de recibir datos desde el subproceso.
	pythonProcess.stdout.on('end', function() {
		const respF = a + ", sos medio uhghjhg" + b +  ", tambien del back"
		res.json({respF});
	})

	// stdin: Se encarga del ingreso de datos al stdin del subproceso. En este caso, envía datos del subproceso de Python.
	// .stdin.write(datos): Envía datos al subproceso
	pythonProcess.stdin.write(req.body.nombre)
	// .stdin.end(): Indica al subproceso que el envío de datos finalizó para que pueda ejecutar sus acciones
	pythonProcess.stdin.end()


});

app.listen(3000, () => {
	console.log(`Servidor escuchando en http://localhost: 3000`);
});
 //LO MODIFIQUE DESDE EL FRONTTTTT