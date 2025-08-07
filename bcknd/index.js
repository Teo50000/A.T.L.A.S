//https://geekflare.com/es/handling-files-in-javascript/

import express from 'express';
import fs from 'fs';
import { spawn } from 'child_process';

const app = express();
app.use(express.json());


console.log("jauduiudu")

fs.appendFile("./index.js", "\n//ya se usar appendFile \n//YA TERMINE PROYECTO \n//na mentira", (err) =>{
    if (err) throw err;
   console.log("¡Completado!");
});
//ya se usar appendFile 
//YA TERMINE PROYECTO 
//na mentira