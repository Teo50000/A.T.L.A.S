//https://geekflare.com/es/handling-files-in-javascript/

import express from 'express';
import fs from 'fs';
import { spawn } from 'child_process';

const app = express();
app.use(express.json());

