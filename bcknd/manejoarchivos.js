import express from 'express';
import fs from 'fs';
import { spawn } from 'child_process';

const app = express();
app.use(express.json());
let respuesta = ""

const cambia = function (carpeta, archivoAC){
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
const elimina = function (carpeta, archivoAE){
fs.unlink(carpeta + archivoAE, (err) =>{
  if(err){
    respuesta = `Lo lamentamos, el archivo que desea eliminar no existe. Intenta ver si esta en otra carpeta o posee un nombre similar`
    return;
  }
  respuesta = `${archivoAE} fue eliminado exitosamente.`
})
}
const copiar = function (carpetaVieja, carpetaNueva, archivoACo){
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
const mover = function (carpetadelaquehayquesacar, carpetaenlaquehayqueponer, archivoAM){
copiar(carpetadelaquehayquesacar, carpetaenlaquehayqueponer, archivoAM, (err) => {
  if (err) {
    console.log("Error en copiar:", err.message);
    return; // 🚨 No seguimos si copiar falla
  }
  elimina(carpetadelaquehayquesacar, archivoAM); // solo se llama si copiar tuvo éxito
});
}

// investigar fs.readdir
const buscNombre = function (params) {
    
}
const buscTipo = function (params){

}




const manejoarch = {
    cambia,
    elimina,
    copiar,
    mover,
    respuesta
}
export default manejoarch;